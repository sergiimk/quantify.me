package measure.io

import com.fasterxml.jackson.core.{JsonFactory, JsonToken, JsonParser}
import org.joda.time.DateTime
import java.io.{InputStream, File}

///////////////////////////////////////////////////////////////////////////////

object MeasureReaderJson {

  def apply(stream: InputStream) = {
    val factory = new JsonFactory()
    val parser = factory.createParser(stream)
    new MeasureReaderJson(parser)
  }

  def apply(file: File) = {
    val factory = new JsonFactory()
    val parser = factory.createParser(file)
    new MeasureReaderJson(parser)
  }

  def apply(json: String) = {
    val factory = new JsonFactory()
    val parser = factory.createParser(json)
    new MeasureReaderJson(parser)
  }

}

///////////////////////////////////////////////////////////////////////////////

class MeasureReaderJson(parser: JsonParser) extends MeasureReader {
  private var isAtStart = true

  private var id = -1L
  private var timestamp: DateTime = null
  private var archtype: String = null

  def isAtMeasure() = archtype != null

  def currentID() = id

  def currentTimestamp() = timestamp

  def currentArchtype() = archtype

  def close() {
    parser.close()
  }

  def nextMeasure() = {
    clearMeasureData()

    if(!isAtStart)
      scanToEnd()

    scanToStart()

    if(parser.getCurrentToken != JsonToken.START_OBJECT) {
      false
    }
    else {
      initMeasureData()
      true
    }
  }

  def nextAttribute() : (String, String) = {
    if(parser.nextToken == JsonToken.END_OBJECT)
      null
    else {
      val name = parser.getText
      parser.nextToken
      (name, parser.getText)
    }
  }

  private def scanToStart() {
    if(isAtStart) {
      parser.nextToken()
      isAtStart = false
    }

    while (parser.getCurrentToken != null
      && parser.getCurrentToken != JsonToken.START_OBJECT)
    {
      parser.nextToken()
    }
  }

  private def scanToEnd() {
    while (parser.getCurrentToken != null
      && parser.getCurrentToken != JsonToken.END_OBJECT)
    {
      parser.nextToken()
    }
  }

  private def clearMeasureData() {
    id = -1
    timestamp = null
    archtype = null
  }

  private def initMeasureData() {
    assert(parser.getCurrentToken == JsonToken.START_OBJECT)

    // id
    parser.nextToken()
    if(parser.getCurrentName != "id")
      throw new RuntimeException("invalid format")
    parser.nextToken()
    id = parser.getText.toLong

    // time
    parser.nextToken()
    if(parser.getCurrentName != "ts")
      throw new RuntimeException("invalid format")
    parser.nextToken()
    timestamp = new DateTime(parser.getText)

    // type
    parser.nextToken()
    if(parser.getCurrentName != "type")
      throw new RuntimeException("invalid format")
    parser.nextToken()
    archtype = parser.getText
  }
}
