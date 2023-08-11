# py-alb-analyzer
A simple python snippet to analyze AWS application load balancer (ALB) logs

## Example usage
Download a bunch of ALB log files from S3 and analyze them for 502 errors:

```bash
$ s3_bucket="your-bucket-name" && prefix="/path/to/prefix/" && aws s3 ls s3://$s3_bucket/$prefix | colrm 1 31 | xargs -P 8 -I % aws s3 cp s3://$s3_bucket/$prefix% /download/path/
$ zcat /download/path/* | python py-alb-analyzer.py --filter elb_status_code=502
```