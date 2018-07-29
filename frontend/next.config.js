// monkeypatch to prevent creating URLs as /page/index.html instead of /page
require('next/router')._rewriteUrlForNextExport = url => url

module.exports = {
  exportPathMap: async function (pathMap) {
    delete pathMap['/index']
    return pathMap
  }
}
