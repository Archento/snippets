/**
 * Helper to repeat a function
 * @description Repeats the given callback function for the specified amount
 * @param {Function} callback the function that is to be repeated
 * @param {Number} interval Time in ms (1000 = 1 second)
 * @param {Number} [repetitions] Number of repetitions; null for indefinitely
 * @param {Boolean} [immediate] Start now or after the given interval
 * @return {Function} Function handler
 */
export function repeater (callback, interval, repetitions, immediate) {
  repetitions = typeof repeat === 'undefined' ? -1 : repetitions
  interval = interval <= 0 ? 1000 : interval
  immediate = typeof immediate === 'undefined' ? false : immediate
  const offset = immediate ? 0 : 1
  let id = null
  if (repetitions > 0) {
    for (let i = 0; i < repetitions; i++) {
      id = setTimeout(callback, interval * (i + offset))
    }
  } else {
    callback()
    id = setInterval(callback, interval)
  }
  return id
}
