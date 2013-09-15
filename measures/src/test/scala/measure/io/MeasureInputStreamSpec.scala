package measure.io

import org.scalatest._
import org.scalatest.matchers._

class MeasureInputStreamSpec extends FlatSpec with ClassicMatchers {

  "Input Stream" should "handle empty stream" in {
    val reader = MeasureReaderJson("")
    val stream = new MeasureInputStream(reader)
    val list = stream.toList
    assert(list.length == 0)
  }

  it should "handle reading from start" in {
    val json =
      """{"id": 1, "ts": "2010-02-01", "type": "location", "city": "Kiev"}
        |{"id": 2, "ts": "2010-02-02", "type": "location", "city": "Dublin"}
        |{"id": 3, "ts": "2010-02-03", "type": "location", "city": "Vancouver"}
      """.stripMargin

    val reader = MeasureReaderJson(json)
    val stream = new MeasureInputStream(reader)
    val list = stream.toList

    assert(list.length == 3)
    assert(list(0).id == 1)
    assert(list(1).id == 2)
    assert(list(2).id == 3)
  }

  it should "handle reading from middle" in {
    val json =
      """{"id": 1, "ts": "2010-02-01", "type": "location", "city": "Kiev"}
        |{"id": 2, "ts": "2010-02-02", "type": "location", "city": "Dublin"}
        |{"id": 3, "ts": "2010-02-03", "type": "location", "city": "Vancouver"}
      """.stripMargin

    val reader = MeasureReaderJson(json)
    reader.nextMeasure()
    reader.nextMeasure()

    val stream = new MeasureInputStream(reader)
    val list = stream.toList

    assert(list.length == 2)
    assert(list(0).id == 2)
    assert(list(1).id == 3)
  }

}
