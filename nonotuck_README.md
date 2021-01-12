# Setup

## Set up the google drive client utility
Download and install the google drive utility: https://github.com/prasmussen/gdrive

``` bash
brew install gdrive
```

Or if setting up on a server use the compile from source approach: https://github.com/prasmussen/gdrive#compile-from-source

Moving forward to get the files use the gdrive download command to suck down the whole submission files directories. The file manipulation code will traverse these directories.

## Configure scripts
Copy nonotuck_config-tristan.py to nonotuck_config-ENVIRONMENT.py replacing ENVIRONMENT with the current environment. Change the values to match your current environment. Create a symlink from this new file to nonotuck_config.py.

```
ln -s nonotuck_config-ENVIRONMENT.py nonotuck_config.py
```

If desired, commit the new config file to the git repository.

```
git add nonotuck_config-ENVIRONMENT.py
```

Don't worry, the symlink will NOT be committed, because it's in the .gitignore file.

The Nonotuck scripts will now read the configuration on execution.
