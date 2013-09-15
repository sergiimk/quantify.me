package measure.io

import measure.Measure

///////////////////////////////////////////////////////////////////////////////

object MeasureInputStream {

  def measureFromReader(reader: MeasureReader) = {
    if(!reader.isAtMeasure())
      throw new IllegalStateException("reader is not at the measure")

    val id = reader.currentID()
    val ts = reader.currentTimestamp()
    val tp = reader.currentArchtype()

    new Measure(id, ts, tp, Map())
  }
}

///////////////////////////////////////////////////////////////////////////////

class MeasureInputStream(reader: MeasureReader) extends Iterable[Measure] {

  /////////////////////////////////////////////////////////

  private class MeasureIterator
    extends Iterator[Measure] {

    def hasNext = {
      if(!reader.isAtMeasure())
        reader.nextMeasure()
      else
        true
    }

    def next() = {
      val measure = MeasureInputStream.measureFromReader(reader)
      reader.nextMeasure()
      measure
    }
  }

  /////////////////////////////////////////////////////////

  def iterator: Iterator[Measure] = new MeasureIterator

}
