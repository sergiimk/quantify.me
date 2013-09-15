package measure.io

import com.fasterxml.jackson.core.{JsonEncoding, JsonFactory, JsonGenerator}
import org.joda.time.DateTime
import java.io.{OutputStream, File}

///////////////////////////////////////////////////////////////////////////////

object MeasureWriterJson {

  def apply(stream: OutputStream) = {
    val factory = new JsonFactory()
    val generator = factory.createGenerator(stream)
    new MeasureWriterJson(generator)
  }

  def apply(file: File, encoding: JsonEncoding) = {
    val factory = new JsonFactory()
    val generator = factory.createGenerator(file, encoding)
    new MeasureWriterJson(generator)
  }

}

///////////////////////////////////////////////////////////////////////////////

class MeasureWriterJson(writer: JsonGenerator) extends MeasureWriter {

  def writeStart(id: Long, timestamp: DateTime, archtype: String) {
    writer.writeStartObject()
    writer.writeFieldName("id")
    writer.writeNumber(id)
    writer.writeFieldName("ts")
    writer.writeString(timestamp.toString)
    writer.writeFieldName("type")
    writer.writeString(archtype)
  }

  def writeAttribute(name: String, value: String) {
    writer.writeFieldName(name)
    writer.writeString(value)
  }

  def writeEnd() {
    writer.writeEndObject()
  }

  def close() {
    writer.close()
  }

}
