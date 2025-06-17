/* global fetch, alert */

/**
 * File download function
 * @description download a file from a
 * @export self
 * @param {String} destinationUrl
 * @param {String} filename
 */
export function download (destinationUrl, filename) {
  fetch(destinationUrl)
    .then(resp => resp.blob())
    .then(blob => {
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.style.display = 'none'
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      alert('Finished downloading file')
    })
    .catch((error) => {
      console.error(error)
    })
}

// example
const el = document.getElementById('download-report-button')

el.addEventListener('click', () => {
  const url = '/download/report'
  const filename = 'report_file.csv'
  download(url, filename)
})
