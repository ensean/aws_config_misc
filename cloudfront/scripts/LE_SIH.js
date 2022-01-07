'use strict';

exports.handler = (event, context, callback) => {
    const alt_dist_base = 'https://xxxxx.cloudfront.net/'
    const response = event.Records[0].cf.response;
    const request = event.Records[0].cf.request;
    const uri = request['uri'];
    // get obj key from uri
    // https://github.com/aws-solutions/serverless-image-handler/blob/1bc3f9fab20582aef6cf107c8390884258172f9c/source/image-handler/image-request.ts#L219
    const obj_key = decodeURIComponent(uri.replace(/\/\d+x\d+:\d+x\d+\/|(?<=\/)\d+x\d+\/|filters:[^/]+|\/fit-in(?=\/)|^\/+/g, '').replace(/^\/+/, ''));
    /**
     * This function updates the HTTP status code in the response to 302, to redirect to another
     * path (cache behavior) that has a different origin configured. Note the following:
     * 1. The function is triggered in an origin response
     * 2. The response status from the origin server is an error status code (4xx or 5xx)
     */

    if (response.status == 413) {
        const redirect_path = alt_dist_base + obj_key;

        response.status = 301;
        response.statusDescription = 'Found';

        /* Drop the body, as it is not required for redirects */
        response.body = '';
        response.headers['location'] = [{ key: 'Location', value: redirect_path }];
    }

    callback(null, response);
};