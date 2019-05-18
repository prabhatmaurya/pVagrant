**Storage Versioning**
$ export storage_name=_name of storage bucket_
## Get staus of bicket versioning
$ gsutil versioning get gs://$storage
## Enable versioning
$ gsutil versioning set on gs://$storage

## Copy a file
$ touch file1
$ gsutil cp file1 gs://$storage

## list a file
$ gsutil ls -a gs://$storage


