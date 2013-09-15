package measure.io

import org.joda.time.DateTime

trait MeasureReader {
  def isAtMeasure(): Boolean

  def currentID(): Long
  def currentTimestamp(): DateTime
  def currentArchtype(): String

  def nextMeasure(): Boolean
  def nextAttribute(): (String, String)

  def close()
}
