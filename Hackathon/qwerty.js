const AWS = require('aws-sdk');
// Enter copied or downloaded access ID and secret key here
const ID = 'AKIAI43MM4QUVYVDT5WA';
const SECRET = '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';

// The name of the bucket that you have created
const BUCKET_NAME = 'hasramtan';
const s3 = new AWS.S3({
    accessKeyId: ID,
    secretAccessKey: SECRET
});
const params = {
    Bucket: BUCKET_NAME,
    CreateBucketConfiguration: {
        // Set your region here
        LocationConstraint: "ap-south-1"//"eu-west-1"
    }
};

s3.createBucket(params, function(err, data) {
    if (err) console.log(err, err.stack);
    else console.log('Bucket Created Successfully', data.Location);
});