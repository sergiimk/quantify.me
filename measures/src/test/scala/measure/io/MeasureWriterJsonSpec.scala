package measure.io

import org.scalatest._
import org.scalatest.matchers._
import org.joda.time.DateTime
import java.io.ByteArrayOutputStream

class MeasureWriterJsonSpec extends FlatSpec with ClassicMatchers {

  "Json Writer" should "write measure header" in {
    val byteStream = new ByteArrayOutputStream()
    val writer = MeasureWriterJson(byteStream)

    writer.writeStart(1, new DateTime(2010, 1, 2, 0, 0, 0), "location")
    writer.writeEnd()
    writer.close()

    val json = new String(byteStream.toByteArray())
    assert(json == """{"id":1,"ts":"2010-01-02T00:00:00.000+02:00","type":"location"}""")
  }

  it should "write attributes" in {
    val byteStream = new ByteArrayOutputStream()
    val writer = MeasureWriterJson(byteStream)

    writer.writeStart(1, new DateTime(2010, 1, 2, 0, 0, 0), "location")
    writer.writeAttribute("city", "Kiev")
    writer.writeAttribute("mood", "sad")
    writer.writeEnd()
    writer.close()

    val json = new String(byteStream.toByteArray())
    assert(json == """{"id":1,"ts":"2010-01-02T00:00:00.000+02:00","type":"location","city":"Kiev","mood":"sad"}""")
  }

}
