package measure.io

import org.scalatest._
import org.scalatest.matchers._
import org.joda.time.DateTime
import java.io.ByteArrayInputStream


class MeasureReaderJsonSpec extends FlatSpec with ClassicMatchers {

  "Json Reader" should "return nothing on empty stream" in {
    val emptyStream = new ByteArrayInputStream(new Array[Byte](0))
    val reader = MeasureReaderJson(emptyStream)

    assert(!reader.nextMeasure())
  }

  it should "read measure header" in {
    val json = """{"id": 1, "ts": "2010-02-01", "type": "location", "city": "Kiev"}"""
    val reader = MeasureReaderJson(json)

    assert(reader.nextMeasure())
    assert(reader.currentID() == 1)
    assert(reader.currentTimestamp() == new DateTime(2010, 2, 1, 0, 0, 0))
    assert(reader.currentArchtype() == "location")

    assert(!reader.nextMeasure())
  }

  it should "read multiple metrics from stream" in {
    val json =
      """{"id": 1, "ts": "2010-02-01", "type": "location", "city": "Kiev"}
        |{"id": 2, "ts": "2010-02-02", "type": "location", "city": "Dublin"}
        |{"id": 3, "ts": "2010-02-03", "type": "location", "city": "Vancouver"}
      """.stripMargin

    val reader = MeasureReaderJson(json)

    assert(reader.nextMeasure())
    assert(reader.nextMeasure())
    assert(reader.nextMeasure())

    assert(reader.currentID() == 3)
    assert(reader.currentTimestamp() == new DateTime(2010, 2, 3, 0, 0, 0))
    assert(reader.currentArchtype() == "location")

    assert(!reader.nextMeasure())
  }

  it should "read measure attributes" in {
    val json = """{"id": 1, "ts": "2010-02-01", "type": "location", "city": "Kiev", "mood": "sad"}"""
    val reader = MeasureReaderJson(json)

    assert(reader.nextMeasure())
    assert(reader.nextAttribute() == ("city", "Kiev"))
    assert(reader.nextAttribute() == ("mood", "sad"))
    assert(reader.nextAttribute() == null)
  }

}
