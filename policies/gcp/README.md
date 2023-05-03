# Custodian-GCP-Policies
[TOC]
### Getting started
#### Quick-install
Reffer [here](https://gitlab.cloudarmour.ai/cspm/custodian_policies/-/tree/development/#quick-install "here") for initial installation.
```shell
#Open Terminal
pip install c7n_gcp
```
#### Connect GCloud with Custodian
Connect Your Authentication Credentials¶

In order for Custodian to be able to interact with your GCP resources, you will need to configure your GCP authentication credentials on your system in a way in which the application is able to retrieve them.

Choose from one of the following methods to configure your credentials, depending on your use case. In either option, after the configuration is complete, Custodian will implicitly pick up your credentials when it runs.
GCP CLI¶

If you are a general user accessing a single account, then you can use the GCP CLI to configure your credentials.

First, install gcloud (the GCP Command Line Interface).

Then run the following command, substituting your username:

gcloud auth application-default login

Executing the command will open a browser window with prompts to finish configuring your credentials. For more information on this command, view its documentation.
Environment Variables¶

If you are planning to run Custodian using a service account, then configure your credentials using environment variables.

Follow the steps outlined in the GCP documentation to configure credentials for service accounts.
#### For Windows
##### With gcloud login


Install gcloud in your local
Run in Terminal `gcloud auth application-default login`
##### Without gcloud login
- Open Run `ctrl+R`
- Search `%appdata%`
- navigate to  *gcloud* directory