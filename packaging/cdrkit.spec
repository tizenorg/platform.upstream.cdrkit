Name:           cdrkit
Version:        1.1.11
Release:        0
Summary:        Tool for Writing CDRs
License:        GPL-2.0
Url:            http://cdrkit.org/
Group:          Applications/Other
Source0:        http://cdrkit.org/releases/cdrkit-%{version}.tar.gz
Source1:        scan_scsi.linux
Source2:        cdinfo.c
BuildRequires:  cmake
BuildRequires:  fdupes
BuildRequires:  file-devel
BuildRequires:  gcc-c++
BuildRequires:  bzip2-devel 
BuildRequires:  libcap-devel
BuildRequires:  perl
BuildRequires:  zlib-devel
Provides:       wodim    = %{version}
Provides:       cdrecord = %{version}
Obsoletes:      cdrecord < %{version}

%description
wodim is used to record data or audio CDs on a CD-Recorder or to write
DVD media on a DVD-Recorder.

%package -n cdrkit-devel-static
License:        GPL-2.0
Summary:        Tool for Writing CDRs - Files Mandatory for Development
Group:          Development/Libraries
Provides:       cdrecord-devel = %{version}
Provides:       cdrtools-devel = %{version}
Provides:       wodim-devel = %{version}
Obsoletes:      cdrecord-devel < %{version}
Obsoletes:      cdrtools-devel < %{version}
Obsoletes:      wodim-devel < %{version}

%description -n cdrkit-devel-static
This package contains cdrkit libraries mandatory for development.

%package -n genisoimage
License:        GPL-2.0
Summary:        A Program for Creating CDs in Linux
Group:          Applications/Other
Recommends:     zisofs-tools
Provides:       mkisofs = %{version}
Obsoletes:      mkisofs < %{version}

%description -n genisoimage
Genisoimage is a pre-mastering program that generates an iso9660
filesystem. It takes a snapshot of a given directory tree, and
generates a binary image which corresponds to an iso9660 filesystem
that can be written to a block device.

%package -n icedax
License:        GPL-2.0
Summary:        A CD-Audio Grabbing tool
Group:          Applications/Other
Requires:       vorbis-tools
Provides:       cdda2wav = %{version}
Obsoletes:      cdda2wav < %{version}

%description -n icedax
The common CD-audio grabbing tool for Linux. The sources are now
contained in the wodim source archive.

%package -n cdrkit-cdrtools-compat
License:        GPL-2.0
Summary:        Tool for Writing CDRs - cdrtools Compatibility Package
Group:          Applications/Other
Requires:       genisoimage = %{version}-%{release}
Requires:       icedax = %{version}-%{release}
Requires:       wodim = %{version}-%{release}

%description -n 'cdrkit-cdrtools-compat'
This package contains these compatibility symlinks:
cdrecord -> wodim
mkisofs -> genisoimage
cdda2wav -> icedax
Install this package if you can't use the cdrkit programs directly.

Requires:       genisoimage = %%{version-%%{release}
Requires:       wodim = %%{version-%%{release}
%prep
%setup -q -n cdrkit-%{version}
# Fix perl path
find . -type f -print0 | xargs -0 perl -pi -e 's#/usr/local/bin/perl#/usr/bin/perl#g'
# Fix permissions (no executables in doc files)
chmod 644 doc/icedax/tracknames.pl misc/burnstuff misc/rc.pp
# Rename in order to not conflict with doc/genisoimage/README when added in genisoimage rpm doc files
mv genisoimage/diag/README genisoimage/diag/README.diag

%build
export CFLAGS="%{optflags} -fno-strict-aliasing -DPIC -fPIC"
export CXXFLAGS="$CFLAGS"

mkdir build
cd build

cmake ../ -DCMAKE_INSTALL_PREFIX=%{_prefix}
make VERBOSE=1 MANDIR=share/man %{?_smp_mflags}
gcc %{optflags} %{S:2} -o cdinfo
cd ..

%install
cd build
%make_install
cd ..

# Fix perl version requirement
perl -pi -e 's#^require v5.8.1;##g' %{buildroot}%{_bindir}/dirsplit

# Install additional programs
install -pm 0755 build/cdinfo \
	         icedax/cdda2mp3.new \
                 icedax/inf2cdtext.pl \
                 %{S:1} \
                 %{buildroot}%{_bindir}
install -pm 0755 3rd-party/geteltorito/geteltorito.pl %{buildroot}%{_bindir}/geteltorito

ln -sf wodim %{buildroot}%{_bindir}/cdrecord
ln -sf wodim %{buildroot}%{_bindir}/dvdrecord
ln -sf readom %{buildroot}%{_bindir}/readcd
ln -sf icedax %{buildroot}%{_bindir}/cdda2wav
ln -sf genisoimage %{buildroot}%{_bindir}/mkhybrid
ln -sf genisoimage %{buildroot}%{_bindir}/mkisofs
ln -sf wodim.1%{ext_man} %{buildroot}%{_mandir}/man1/cdrecord.1%{ext_man}
ln -sf readom.1%{ext_man} %{buildroot}%{_mandir}/man1/readcd.1%{ext_man}
ln -sf icedax.1%{ext_man} %{buildroot}%{_mandir}/man1/cdda2wav.1%{ext_man}

ln -sf genisoimage.1%{ext_man} %{buildroot}%{_mandir}/man1/mkisofs.1%{ext_man}
ln -sf cdda2ogg.1%{ext_man} %{buildroot}%{_mandir}/man1/cdda2mp3.1%{ext_man}

# Install libraries
cd build
install -dm 0755 %{buildroot}%{_libdir}
install -pm 0644 libedc/libedc.a \
                 libhfs_iso/libhfs_iso.a \
                 libparanoia/libparanoia.a \
                 librols/librols.a \
                 libunls/libunls.a \
                 libusal/libusal.a \
                 %{buildroot}%{_libdir}
cd ..

# Install headers
rm -rf %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_includedir}/cdrkit
cp -a include/*.h %{buildroot}%{_includedir}/cdrkit
cp -a libusal/usal %{buildroot}%{_includedir}/
cp -a libusal/*.h %{buildroot}%{_includedir}/usal/
# it seems to depend on the cmake version if xconfig.h lands in ./ or in ./include/
# I don't know why, a cmake expert should fix that. Work around it for now.
cd build
if test -e xconfig.h; then # old cmake 2.6
	cp -a xconfig.h %{buildroot}%{_includedir}/cdrkit
elif ! test -e include/xconfig.h; then # new cmake 2.8
	echo "error: xconfig.h not found!"
	false
fi
cd ..

# Install config files
install -dm 0755 %{buildroot}%{_sysconfdir}
install -pm 0644 netscsid/netscsid.dfl %{buildroot}%{_sysconfdir}/netscsid.conf
install -pm 0644 wodim/wodim.dfl %{buildroot}%{_sysconfdir}/wodim.conf

# Missing man page. Do symlink like in Debian.
ln -sf wodim.1%{ext_man} %{buildroot}%{_mandir}/man1/netscsid.1%{ext_man}

%fdupes -s %{buildroot}

%clean
rm -rf %{buildroot}

%verifyscript
%verify_permissions -e %{_bindir}/wodim

%post
%if 0%{?set_permissions:1} > 0
  %{set_permissions wodim}
%else
  %{run_permissions}
%endif

%files
%defattr(-,root,root,-)
%license COPYING
%config(noreplace) %{_sysconfdir}/netscsid.conf
%config(noreplace) %{_sysconfdir}/wodim.conf
%{_bindir}/cdinfo
%{_bindir}/readom
%verify(not mode) %attr(0755,root,root) %{_bindir}/wodim
%attr(0555,root,root) %{_sbindir}/netscsid
%doc %{_mandir}/man1/netscsid.1%{ext_man}
%doc %{_mandir}/man1/readom.1%{ext_man}
%doc %{_mandir}/man1/wodim.1%{ext_man}

%files -n cdrkit-cdrtools-compat
%defattr(-,root,root,-)
%{_bindir}/cdda2wav
%{_bindir}/cdrecord
%{_bindir}/dvdrecord
%{_bindir}/mkhybrid
%{_bindir}/mkisofs
%{_bindir}/readcd
%doc %{_mandir}/man1/cdda2wav.1%{ext_man}
%doc %{_mandir}/man1/cdrecord.1%{ext_man}
%doc %{_mandir}/man1/mkisofs.1%{ext_man}
%doc %{_mandir}/man1/readcd.1%{ext_man}

%files -n cdrkit-devel-static
%defattr(-,root,root,-)
%{_includedir}/cdrkit/
%{_includedir}/usal/
%{_libdir}/lib*.a

%files -n genisoimage
%defattr(-,root,root,-)
%{_bindir}/devdump
%{_bindir}/dirsplit
%{_bindir}/genisoimage
%{_bindir}/geteltorito
%{_bindir}/isodebug
%{_bindir}/isodump
%{_bindir}/isoinfo
%{_bindir}/isovfy
%doc %{_mandir}/man1/devdump.1%{ext_man}
%doc %{_mandir}/man1/dirsplit.1%{ext_man}
%doc %{_mandir}/man1/genisoimage.1%{ext_man}
%doc %{_mandir}/man1/isodebug.1%{ext_man}
%doc %{_mandir}/man1/isodump.1%{ext_man}
%doc %{_mandir}/man1/isoinfo.1%{ext_man}
%doc %{_mandir}/man1/isovfy.1%{ext_man}
%doc %{_mandir}/man5/genisoimagerc.5%{ext_man}

%files -n icedax
%defattr(-,root,root,-)
%{_bindir}/cdda2mp3
%{_bindir}/cdda2mp3.new
%{_bindir}/cdda2ogg
%{_bindir}/icedax
%{_bindir}/inf2cdtext.pl
%{_bindir}/pitchplay
%{_bindir}/readmult
%{_bindir}/scan_scsi.linux
%doc %{_mandir}/man1/cdda2mp3.1%{ext_man}
%doc %{_mandir}/man1/cdda2ogg.1%{ext_man}
%doc %{_mandir}/man1/icedax.1%{ext_man}
%doc %{_mandir}/man1/list_audio_tracks.1%{ext_man}
%doc %{_mandir}/man1/pitchplay.1%{ext_man}
%doc %{_mandir}/man1/readmult.1%{ext_man}

