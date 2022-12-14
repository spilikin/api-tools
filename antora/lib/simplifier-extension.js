'use strict'
const https = require('https');
const request = require('sync-request');

const warninig = "Usage: simplifier::render[project=PROJECT_NAME,resource=RESOURCE_NAME]"


function loadUsingPromise(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (resp) => {
        let data = '';

        // A chunk of data has been recieved.
        resp.on('data', (chunk) => {
            data += chunk;
        });

        // The whole response has been received. Print out the result.
        resp.on('end', () => {
            resolve(data);
        });

    }).on("error", (err) => {
        reject(err);
    });
  });
} 

async function load(url) {
  return await loadUsingPromise(url).then((data) => { return data })
}

module.exports.register = function (registry) {
  registry.blockMacro(function () {
    var self = this
    self.named('simplifier')
    self.process(function (parent, target, attrs) {
      if (attrs.project == null || attrs.resource == null) {
        console.warn("Invalid usage of simplifier macro.")
        return self.createBlock(parent, 'paragraph', warninig)
      } else {
        const simplifierUrl = `https://simplifier.net/embed/render?id=${attrs.project}/${attrs.resource}`

        var renderedResource = request('GET', simplifierUrl).getBody('utf8');

        renderedResource = renderedResource.replaceAll("src=\"/", "src=\"https://simplifier.net/")
        renderedResource = renderedResource.replaceAll("href=\"/", "href=\"https://simplifier.net/")

        var renderedResource = renderedResource + "<br><br>"+ request('GET', "https://simplifier.net/ui/packagefile/renderoverview?packageFileId=319737").getBody('utf8');

        return self.createPassBlock(parent, `<div class="simiplifier-resource>${renderedResource}</div>`)
      }
       
    })
  })
}
