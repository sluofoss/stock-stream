# file system organization
```
   📂 yahoo-finance-cron
      📂 dev
         📂 data_store
         📂 vpc
         📂 pipeline
      📂 staging
         📂 data_store
         📂 vpc
         📂 pipeline   
      📂 prod
         📂 data_store
         📂 vpc
         📂 pipeline
      📂 modules
         📂 data_store
            store for the results from lambda, include permanent s3 buckets
         📂 vpc
            store the network config
         📂 pipeline
            defines the lambda, schedule, that should be deployed 
📂 state_store
   📂 modules
      📂 state_store
   📂 dev
   📂 staging
   📂 prod
   
```



# execution order (planned)
```
For each environment in `state_store/`:
   1. `terraform init`, `terraform apply` 

For each environment in `yahoo-finance-cron/`
   For each in `[data_store, vpc, pipeline]`
         1. `terraform init`, `terraform apply` 
```
> [!NOTE] 
for any change to `data_store` and `vpc`, `pipeline` needs to `terraform init` again.
