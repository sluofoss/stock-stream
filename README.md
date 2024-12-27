
# Table of content

- [Table of content](#table-of-content)
- [progress tracking](#progress-tracking)
- [Project Set up:](#project-set-up)
- [aws cli set up](#aws-cli-set-up)
- [aws sso login set up](#aws-sso-login-set-up)
- [stack setup](#stack-setup)
- [](#)
- [explain logic:](#explain-logic)
- [random cmd](#random-cmd)
- [yfinance 1minute asx data size estimate](#yfinance-1minute-asx-data-size-estimate)
- [TODO:](#todo)
- [useful commands:](#useful-commands)

# progress tracking
https://github.com/users/lu0x1a0/projects/1/

# Project Set up:
project board -> issue -> branch -> pr

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

# random cmd
- check the file size under folder
> ls -lRh mocks3yfiance/ > datasize.log
https://askubuntu.com/questions/57603/how-to-list-recursive-file-sizes-of-files-and-directories-in-a-directory

# yfinance 1minute asx data size estimate
8 * 360 * 2000 * 8 * 5 * 52 = 11_980_800_000 \approxeq 12 GB
8 column (ts, OHLCV, dividend, stock split)
360 minute = 10am-4pm (6 hour * 60)
2000 stocks 
8 bytes per number
5 day 
52 weeks 

> 2023-12-14 broken (initial size) 5.63 mb
> a2m <  360 entries, 6kb, 
    > 8 * 360 * 8 = 23040 = 23 kb (so it is compressed) Good!

# TODO: 
- todo in code
    - dump to s3 instead
- check out whether are any of them not pulling data when there are data
- check for correctness of all symbol code info
    - maybe do check by using absence of data over a longer period?
- introduce logging where all logs are put into 1 file.

# useful commands:

Run this in any terraform root module to visualize the corresponding resource dependencies.
```
terraform graph | python -c "import sys; import base64; import zlib; print(base64.urlsafe_b64encode(zlib.compress(sys.stdin.read().encode('utf-8'), 9)).decode('ascii'))" | sed 's/^/ https:\/\/kroki.io\/graphviz\/svg\//'
```