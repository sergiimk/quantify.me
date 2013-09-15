package measure.io

import org.joda.time.DateTime

trait MeasureWriter {
  def writeStart(id: Long, timestamp: DateTime, archtype: String)
  def writeAttribute(name: String, value: String)
  def writeEnd()

  def close()
}
