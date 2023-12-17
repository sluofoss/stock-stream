# aws cli set up 

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

# aws sso login set up 

# stack setup

#

# explain logic:
```mermaid
flowchart
    subgraph lambda_caller
        aws
        mock
    end
    lambda_caller --> id1["awwlambda.getdatabydate(symbols, event_time)"] --> s3_bucket
```