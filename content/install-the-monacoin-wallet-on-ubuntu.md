Title: Install the Monacoin Wallet on Ubuntu
Date: 2017-12-16 23:35
Author: john-sobanski
Category: Coins
Tags: Coins, HOWTO
Slug: install-the-monacoin-wallet-on-ubuntu
Status: published


From the land of Nintendo and Samurai comes [Monacoin](https://github.com/monacoinproject/monacoin), a Japanese cryptographic currency based on [Litecoin](https://translate.google.com/translate?hl=en&sl=ja&u=https://ja.wikipedia.org/wiki/Monacoin).  If you look at [www.coinmarketcap.com](https://coinmarketcap.com/currencies/monacoin/) you will see that Monacoin increased about ***30x*** in the past three months.

![Monacoin]({filename}/images/Install_the_Monacoin_Wallet_on_Ubuntu/Monacoin.png)

I found it a bit challenging to install the Monacoin wallet on Ubuntu.  I worked through the kinks and present to you this simple HOWTO.  The steps include:

  1.  Workstation Prep
     * Update the OS
     * Install the required libraries (packages)
     * Create a dedicated Monacoin user
  2. Berkley DB
     * Create the build directories
     * Download Berkley DB
     * Run the configure script
     * Make and install the Database
  3.  Monacoin wallet
     * Download the Monacoin wallet
     * Run the autogen script
     * Run the configure script
     * Make and install the wallet
  4.  Test Drive the wallet
     * Hello World
     * Generate a new address and private key
     * Wipe the keys
     * Re-import the deleted key and validate

#1.  Workstation Prep
##1.1  Update the OS
We want to first ensure that we have an up to date Operating System.  This will  protect against known security issues and patch any known bugs.

```bash
ubuntu@ip-192-168-10-203:~$ sudo apt-get -y update
Hit:1 http://us-east-1.ec2.archive.ubuntu.com/ubuntu xenial InRelease
Get:2 http://us-east-1.ec2.archive.ubuntu.com/ubuntu xenial-updates InRelease [102 kB]

    ...

    
Get:30 http://security.ubuntu.com/ubuntu xenial-security/main Translation-en [156 kB]
Get:31 http://security.ubuntu.com/ubuntu xenial-security/universe amd64 Packages [168 kB]
Get:32 http://security.ubuntu.com/ubuntu xenial-security/universe Translation-en [88.3 kB]
Get:33 http://security.ubuntu.com/ubuntu xenial-security/multiverse amd64 Packages [2,748 B]
Fetched 12.2 MB in 2s (5,107 kB/s)
Reading package lists... Done
ubuntu@ip-192-168-10-203:~$
```

##1.2.  Install the required libraries (packages)
To use the wallet, we first need to compile the wallet.  To compile the wallet, we must install the required libraries.

```bash
 ubuntu@ip-192-168-10-203:~$ sudo apt-get -y install automake build-essential checkinstall git libboost-dev libboost-system-dev libboost-filesystem-dev libboost-program-options-dev libboost-thread-dev libevent-dev libtool libssl-dev pkg-config
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  autoconf autotools-dev binutils cpp cpp-5 dpkg-dev fakeroot g++ g++-5 gcc gcc-5 libalgorithm-diff-perl
  libalgorithm-diff-xs-perl libalgorithm-merge-perl libasan2 libatomic1 libboost-atomic1.58-dev
  libboost-atomic1.58.0 libboost-chrono1.58-dev libboost-chrono1.58.0 libboost-date-time1.58-dev
  libboost-date-time1.58.0 libboost-filesystem1.58-dev libboost-filesystem1.58.0
  libboost-program-options1.58-dev libboost-program-options1.58.0 libboost-serialization1.58-dev
  libboost-serialization1.58.0 libboost-system1.58-dev libboost-system1.58.0 libboost-thread1.58-dev
  libboost-thread1.58.0 libboost1.58-dev libc-dev-bin libc6-dev libcc1-0 libcilkrts5 libdpkg-perl
  libevent-core-2.0-5 libevent-extra-2.0-5 libevent-openssl-2.0-5 libevent-pthreads-2.0-5 libfakeroot
  libfile-fcntllock-perl libgcc-5-dev libgomp1 libisl15 libitm1 liblsan0 libltdl-dev libltdl7 libmpc3
  libmpx0 libquadmath0 libssl-doc libstdc++-5-dev libtsan0 libubsan0 linux-libc-dev m4 make manpages-dev
  zlib1g-dev

      ...
      
Setting up libssl-dev:amd64 (1.0.2g-1ubuntu4.8) ...
Setting up libssl-doc (1.0.2g-1ubuntu4.8) ...
Setting up libtool (2.4.6-0.1) ...
Setting up manpages-dev (4.04-2) ...
Setting up pkg-config (0.29.1-0ubuntu1) ...
Processing triggers for libc-bin (2.23-0ubuntu9) ...
ubuntu@ip-192-168-10-203:~$
```

##1.3  Create a dedicated Monacoin user
To prevent privilege escalation, we create an independent Monacoin user.  Security best practices dictate that a system administrator create a separate user for each coin.  This way, if a wallet acts up (due to faulty or insecure code), the separation of user space reduces the blast radius.

```bash
ubuntu@ip-192-168-10-203:~$ sudo adduser mona
Adding user `mona' ...
Adding new group `mona' (1001) ...
Adding new user `mona' (1001) with group `mona' ...
Creating home directory `/home/mona' ...
Copying files from `/etc/skel' ...
Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully
Changing the user information for mona
Enter the new value, or press ENTER for the default
        Full Name []: Mona Coin
        Room Number []:
        Work Phone []:
        Home Phone []:
        Other []:
Is the information correct? [Y/n] Y
ubuntu@ip-192-168-10-203:~$
```

Log in as user ***mona*** to locally install a local copy of the [Berkley Database](https://en.wikipedia.org/wiki/Berkeley_DB).

#2. Install the Berkley DB
##2.1  Create the build directories
Create a directory for dependencies and source code.  Then, change directories to enter the source code directory, ***downloads***.

```bash
mona@ip-192-168-10-203:~$ mkdir -p ~/mona/{deps,downloads}
mona@ip-192-168-10-203:~$ cd mona/downloads/
mona@ip-192-168-10-203:~/mona/downloads$
```

##2.2  Download Berkley DB
Download and extract the source code to the Berkley Database.  Since I provide the direct URL, you will not need to set up an Oracle user account.

 > ***NOTE***:  For the wallet to compile, you ***must*** download version ***4.8***.  ***DO NOT*** download the most recent version! 

```bash
# MUST be 4.8
mona@ip-192-168-10-203:~/mona/downloads$  wget http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz
mona@ip-192-168-10-203:~/mona/downloads$  tar -xzvf db-4.8.30.NC.tar.gz
```

##2.3  Run the configure script
Enter the source code directory and execute the configure script.  Notice we tell the compiler to place the (soon to be) compiled binaries into the (currently empty) dependencies directory we just created.  If you see any errors, double check to see if you (or I) forgot to install a needed library.

```bash
mona@ip-192-168-10-203:~/mona/downloads$  cd db-4.8.30.NC/build_unix   
mona@ip-192-168-10-203:~/mona/downloads/db-4.8.30.NC/build_unix$ ../dist/configure --prefix=/home/mona/mona/deps --enable-cxx
checking build system type... x86_64-unknown-linux-gnu
checking host system type... x86_64-unknown-linux-gnu
checking if building in the top-level or dist directories... no
checking if --disable-cryptography option specified... no
    
    ...
    
    
config.status: creating include.tcl
config.status: creating db.h
config.status: creating db_config.h
config.status: db_config.h is unchanged
config.status: executing libtool commands
mona@ip-192-168-10-203:~/mona/downloads/db-4.8.30.NC/build_unix$
```

##2.4  Make and install the Database
Compile and install the database via the ***make*** utility.  You can ignore any ***conflicting type*** warnings.

```bash
mona@ip-192-168-10-203:~/mona/downloads/db-4.8.30.NC/build_unix$  make && make install
libtool: compile:  cc -c -I. -I../dist/.. -D_GNU_SOURCE -D_REENTRANT -O3 ../dist/../db/db_setlsn.c -o db_setlsn.o >/dev/null 2>&1
./libtool --mode=compile cc -c -I. -I../dist/..  -D_GNU_SOURCE -D_REENTRANT -O3  ../dist/../common/db_shash.c
libtool: compile:  cc -c -I. -I../dist/.. -D_GNU_SOURCE -D_REENTRANT -O3 ../dist/../common/db_shash.c  -fPIC -DPIC -o .libs/db_shash.o
In file included from ../dist/../dbinc/mutex_int.h:12:0,
                 from ../dist/../dbinc/mutex.h:15,
                 from ./db_int.h:884,
                 from ../dist/../common/db_shash.c:11:
../dist/../dbinc/atomic.h:179:19: warning: conflicting types for built-in function ‘__atomic_compare_exchange’
 static inline int __atomic_compare_exchange(
                       ^

    ...

libtool: install: cp -p .libs/db_load /home/mona/mona/deps/bin/db_load
libtool: install: cp -p .libs/db_printlog /home/mona/mona/deps/bin/db_printlog
libtool: install: cp -p .libs/db_recover /home/mona/mona/deps/bin/db_recover
libtool: install: cp -p .libs/db_sql /home/mona/mona/deps/bin/db_sql
libtool: install: cp -p .libs/db_stat /home/mona/mona/deps/bin/db_stat
libtool: install: cp -p .libs/db_upgrade /home/mona/mona/deps/bin/db_upgrade
libtool: install: cp -p .libs/db_verify /home/mona/mona/deps/bin/db_verify
Installing documentation: /home/mona/mona/deps/docs ...
mona@ip-192-168-10-203:~/mona/downloads/db-4.8.30.NC/build_unix$
```

#3.  Install the Monacoin wallet
#3.1  Download the Monacoin wallet
Go back to the ***downloads*** directory and download the Monacoin source code.

```
mona@ip-192-168-10-203:~/mona/downloads/db-4.8.30.NC/build_unix$  cd ~/mona/downloads/
mona@ip-192-168-10-203:~/mona/downloads$  git clone https://github.com/monacoinproject/monacoin.git
mona@ip-192-168-10-203:~/mona/downloads$   git clone https://github.com/monacoinproject/monacoin.git
Cloning into 'monacoin'...
remote: Counting objects: 91854, done.
remote: Total 91854 (delta 0), reused 0 (delta 0), pack-reused 91854
Receiving objects: 100% (91854/91854), 89.89 MiB | 24.50 MiB/s, done.
Resolving deltas: 100% (62407/62407), done.
Checking connectivity... done.
```

##3.2  Run the autogen script
The Monacoin wallet requires an extra step before we run the configure script.  We must first run [autogen](https://www.gnu.org/software/autogen/).  Extract the downloaded source code and enter the source directory.

```bash
mona@ip-192-168-10-203:~/mona/downloads$ cd monacoin
mona@ip-192-168-10-203:~/mona/downloads/monacoin$  ./autogen.sh
mona@ip-192-168-10-203:~/mona/downloads/monacoin$ ./autogen.sh
libtoolize: putting auxiliary files in AC_CONFIG_AUX_DIR, 'build-aux'.
libtoolize: copying file 'build-aux/ltmain.sh'
libtoolize: putting macros in AC_CONFIG_MACRO_DIRS, 'build-aux/m4'.
libtoolize: copying file 'build-aux/m4/libtool.m4'
libtoolize: copying file 'build-aux/m4/ltoptions.m4'

    ...

configure.ac:32: installing 'build-aux/missing'
Makefile.am:12: warning: user variable 'GZIP_ENV' defined here ...
/usr/share/automake-1.15/am/distdir.am: ... overrides Automake variable 'GZIP_ENV' defined here
src/Makefile.am: installing 'build-aux/depcomp'
src/Makefile.am:505: warning: user target '.mm.o' defined here ...
/usr/share/automake-1.15/am/depend2.am: ... overrides Automake target '.mm.o' defined here
parallel-tests: installing 'build-aux/test-driver'
mona@ip-192-168-10-203:~/mona/downloads/monacoin$
```

##3.3 Run the configure script
Run the configure script with the flags I supply.  Note that the flag uses the letter ***O*** and not the number zero (***0***).

```bash
# O not 0
$  ./configure CPPFLAGS="-I/home/mona/mona/deps/include -O2" LDFLAGS="-L/home/mona/mona/deps/lib" --prefix=/home/mona/mona
Makefile.am: installing 'build-aux/depcomp'
parallel-tests: installing 'build-aux/test-driver'
libtoolize: putting auxiliary files in AC_CONFIG_AUX_DIR, 'build-aux'.
libtoolize: copying file 'build-aux/ltmain.sh'
libtoolize: putting macros in AC_CONFIG_MACRO_DIRS, 'build-aux/m4'.
libtoolize: copying file 'build-aux/m4/libtool.m4'
libtoolize: copying file 'build-aux/m4/ltoptions.m4'
libtoolize: copying file 'build-aux/m4/ltsugar.m4'
libtoolize: copying file 'build-aux/m4/ltversion.m4'
libtoolize: copying file 'build-aux/m4/lt~obsolete.m4'

    ...

Fixing libtool for -rpath problems.

Options used to compile and link:
  with wallet   = yes
  with gui / qt = no
  with zmq      = no
  with test     = no
  with bench    = yes
  with upnp     = auto
  debug enabled = no
  werror        = no

  target os     = linux
  build os      =

  CC            = gcc
  CFLAGS        = -g -O2 -fPIC
  CPPFLAGS      = -I/home/mona/mona/deps/include -O2 -DHAVE_BUILD_INFO -D__STDC_FORMAT_MACROS
  CXX           = g++ -std=c++11
  CXXFLAGS      = -g -O2 -Wall -Wextra -Wformat -Wvla -Wformat-security -Wno-unused-parameter
  LDFLAGS       = -L/home/mona/mona/deps/lib
```

##3.4 Make and install the wallet
Now make and install the wallet.

```bash
mona@ip-192-168-10-203:~/mona/downloads/monacoin$ make && make install
Making all in src
make[1]: Entering directory '/home/mona/mona/downloads/monacoin/src'
make[2]: Entering directory '/home/mona/mona/downloads/monacoin/src'
  CXX      crypto/libbitcoinconsensus_la-aes.lo
  CXX      crypto/libbitcoinconsensus_la-hmac_sha256.lo
  CXX      crypto/libbitcoinconsensus_la-hmac_sha512.lo
  CXX      crypto/libbitcoinconsensus_la-ripemd160.lo
  CXX      crypto/libbitcoinconsensus_la-sha1.lo
  CXX      crypto/libbitcoinconsensus_la-sha256.lo

    ...
    
make[1]: Leaving directory '/home/mona/mona/downloads/monacoin/doc/man'
make[1]: Entering directory '/home/mona/mona/downloads/monacoin'
make[2]: Entering directory '/home/mona/mona/downloads/monacoin'
make[2]: Nothing to be done for 'install-exec-am'.
 /bin/mkdir -p '/home/mona/mona/lib/pkgconfig'
 /usr/bin/install -c -m 644 libbitcoinconsensus.pc '/home/mona/mona/lib/pkgconfig'
make[2]: Leaving directory '/home/mona/mona/downloads/monacoin'
make[1]: Leaving directory '/home/mona/mona/downloads/monacoin'
mona@ip-192-168-10-203:~/mona/downloads/monacoin$
```

#4.  Test Drive the wallet
##4.1 Hello World
Now let\'s take this baby for a spin!  Change directories to the newly created binary directory (***bin***) and execute the freshly compiled ***monacoind*** (Monacoin Daemon) command.

```bash
mona@ip-192-168-10-203:~/mona/downloads/monacoin$ cd ~/mona/bin
mona@ip-192-168-10-203:~/mona/bin$ ./monacoind --printoconsole
./monacoind: error while loading shared libraries: libdb_cxx-4.8.so: cannot open shared object file: No such file or directory
mona@ip-192-168-10-203:~/mona/bin$
```

Whoops.  The Monacoin daemon can't find the Berkley DB library (shared object) we compiled a few steps back.  That's fine, we just need to update our environment variable.  (Add this to your ***[.bashrc](https://unix.stackexchange.com/questions/129143/what-is-the-purpose-of-bashrc-and-how-does-it-work)*** file to make it permanent).

```bash
mona@ip-192-168-10-203:~/mona/bin$  echo 'export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/home/mona/mona/deps/lib"' >> ~/.bashrc
mona@ip-192-168-10-203:~/mona/bin$ source ~/.bashrc
```

Now start the [Daemon](https://kb.iu.edu/d/aiau).

```bash
$ ./monacoind --printtoconsole
    ...a whole bunch of stuff on the screen...
```

Now that we started the Daemon, we can plug into it with the Monacoin client, also known as a [command line interface (CLI)](https://en.wikipedia.org/wiki/Command-line_interface`).  Leave the Daemon's terminal running, and then open a ***NEW*** terminal.  From the new terminal, run these commands:

```bash
# From another terminal
ubuntu@ip-192-168-10-203:~$ sudo su - mona
mona@ip-192-168-10-203:~$ cd mona/bin/
mona@ip-192-168-10-203:~/mona/bin$ ./monacoin-cli getinfo
   ... a whole bunch of stuff on the screen...
```

##4.2 Generate a new address and private key
Now we will generate a new address.  This also generates an associated private keys.  So, we will get to own all the coins sent to the address, as long as we hold on to the private key.

```bash
$ ./monacoin-cli getnewaddress 
MSuRjV1ogf3C7Yys82NvxQ35gacJYoctWk
# The dumpprivkey command shows the private key in a Base58 checksum-encoded format called the Wallet Import Format (WIF)
$ ./monacoin-cli dumpprivkey MSuRjV1ogf3C7Yys82NvxQ35gacJYoctWk
T7PtVHPpHwFbjcuwVA5YBsNShKodoVfgVH796eva13a3Ze9BRhHz
```

Now, if anybody reading this blog sent coins to address ***MSuRjV1ogf3C7Yys82NvxQ35gacJYoctWk***, you can steal them with the private key ***T7PtVHPpHwFbjcuwVA5YBsNShKodoVfgVH796eva13a3Ze9BRhHz***!

##4.3 Wipe the keys
I now present to you a fun experiment.  Kill the Monacoin daemon (***monacoind***) in the other terminall by hitting ***CTRL^C***.  Now completely wipe out the private key database in your wallet.

> ***WARNING***:  Only perform this command in a junk or toy wallet.  ***DO NOT*** execute this command on a wallet that contains coins!!!  Execute at your own risk!  By reading this website you agree I am not liable for any damages whatsoever due to errors on your part.  See this website's [license](https://raw.githubusercontent.com/hatdropper1977/john.sobanski.io/master/LICENSE) for details.

```bash
$ rm -rf ~/.monacoin/*
```

Now, when you run ***monacoind*** you will see that the Daemon cannot find any local keys, so it generates a new database.

```bash
$ ./monacoind --printoconsole
Failed to create backup boost::filesystem::copy_file: No such file or directory: "/home/mona/.monacoin/wallet.dat", "/home/mona/.monacoin/backups/wallet.dat.2017-12-16"
```

OK - now let's see if the new database has the private key associated with the address we generated above.  It won't, because we deleted the private key.

```bash
$ ./monacoin-cli dumpprivkey MSuRjV1ogf3C7Yys82NvxQ35gacJYoctWk
error code: -4
error message:
Private key for address MSuRjV1ogf3C7Yys82NvxQ35gacJYoctWk is not know
```

Now, import the private key...

```bash
$ ./monacoin-cli importprivkey T7PtVHPpHwFbjcuwVA5YBsNShKodoVfgVH796eva13a3Ze9BRhHz <YOUR WALLET'S NAME>
```

As expected, when we query the address ***MSuRjV1ogf3C7Yys82NvxQ35gacJYoctWk***, our client will respond with the private key we just imported.

```bash
$ ./monacoin-cli dumpprivkey MSuRjV1ogf3C7Yys82NvxQ35gacJYoctWk
T7PtVHPpHwFbjcuwVA5YBsNShKodoVfgVH796eva13a3Ze9BRhHz
```

Thanks for showing interest in Monacoin.  If you found this HOWTO useful, send me a Monacoin (or at least some Milibits) to this Monacoint address:

***MMsMR3pcBZrTfXB8qmzuCqbo88dDTEhKyw***
