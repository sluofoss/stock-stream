# file system organization
```
   📂 yahoo-finance-cron
      📂 dev
         📂 storage
         📂 vpc
         📂 pipeline
      📂 staging
         📂 storage
         📂 vpc
         📂 pipeline   
      📂 prod
         📂 storage
         📂 vpc
         📂 pipeline
      📂 modules
         📂 storage
            - store for the results from lambda, include permanent s3 buckets
            - store the artifacts required for deployment (lambda package)
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





# diagram 
![state store dev](https://kroki.io/graphviz/svg/eNq9kr1uAyEQhPt7CkQdX5PScto0qdJaEVpg74yOgxMLjqzI7x4gTSyZyJe_kmVmv0GDNmOA5cAe2VvHWAA3aRPYjvHnJ77NE-c1sj0dYME8DajiHRu8iw7mMuAEjjaEwQz8pegpyY-FXNlEEYOYvU4We4oQUVD0AYXGI688xixItGVRQ1ZFDWC9axh7eCWhT9nltRQRZJbkNAEGH2ZhvZqIs32l7_gN2vq4r2l0L2RSE8ZP5qq7BLVlaxhiSdIaJUApJBKypOwvZg3qDcZVOXIVx9wyGY0CnQqnJRrvhPJuMGMKUE69xgGSja1Iq3asSpfXUjYbN_boSrG6leGKspLO3S82snn45g_adn_Txz8EulbBD7Dn7h2LQruS)