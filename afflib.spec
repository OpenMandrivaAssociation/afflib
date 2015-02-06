%define	major 0
%define libname	%mklibname afflib %{major}
%define develname %mklibname -d afflib

Summary:	A set of programs for creating and manipulating AFF files
Name:		afflib
Version:	3.7.1
Release:	3
Group:		System/Libraries
License:	BSD
URL:		http://www.afflib.org/
Source0:	http://www.afflib.org/downloads/%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(libcurl)
# GPLv2 FOSS incompatible with BSD with advertising
#BuildRequires:	fuse-devel
BuildRequires:	libewf-devel
BuildRequires:	lzma-devel
BuildRequires:	expat-devel
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(python)
# GPLv2 FOSS incompatible with BSD with advertising
#BuildRequires:	readline-devel
BuildRequires:	pkgconfig(zlib)

%description
AFFLIB is an open source library developed by Simson Garfinkel and Basis
Technology that implements the AFF standard. AFFLIB is distributed under
4-clause Berkeley License and may be freely incorporated into both Open
Source and Proprietary software.

In addition to the library, AFFLIB also comes with the AFF Tools, a set of
programs for creating and manipulating AFF files.

%package -n	%{libname}
Summary:	A shared library that implements the AFF standard
Group:		System/Libraries

%description -n	%{libname}
AFFLIB is an open source library developed by Simson Garfinkel and Basis
Technology that implements the AFF standard. AFFLIB is distributed under
4-clause Berkeley License and may be freely incorporated into both Open
Source and Proprietary software.

This package contains a shared library that implements the AFF standard.

%package -n	%{develname}
Summary:	Static library and header files for the afflib library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Requires:	%{libname} = %{version}

%description -n	%{develname}
AFFLIB is an open source library developed by Simson Garfinkel and Basis
Technology that implements the AFF standard. AFFLIB is distributed under
4-clause Berkeley License and may be freely incorporated into both Open
Source and Proprietary software.

This package contains the static afflib library and its header files.

%prep
%setup -q

#fix spurious permissions with lzma443
find lzma443 -type f -exec chmod 0644 {} ';'
chmod 0644 lib/base64.{h,cpp}

%build
%configure2_5x \
	--disable-static \
	--enable-shared \
	--enable-wide-character-type \
	--enable-libewf=yes \
	--enable-s3=yes \
	--enable-fuse=no \
	--enable-python=yes \
	--enable-qemu=no \
	--with-curl=%{_prefix}
%make

%install
%makeinstall_std
# install headers as well
install -d %{buildroot}%{_includedir}/afflib
install -m0644 lib/*.h %{buildroot}%{_includedir}/afflib/

%files
%{_bindir}/affcat
%{_bindir}/affcompare
%{_bindir}/affconvert
%{_bindir}/affcopy
%{_bindir}/affcrypto
%{_bindir}/affdiskprint
%{_bindir}/affix
%{_bindir}/affuse
%{_bindir}/affinfo
%{_bindir}/affrecover
%{_bindir}/affsegment
%{_bindir}/affsign
%{_bindir}/affstats
%{_bindir}/affverify
%{_bindir}/affxml
%{_mandir}/man1/affcat.1*
%{py_platsitedir}/pyaff.so

%files -n %{libname}
%doc AUTHORS BUGLIST.txt COPYING ChangeLog NEWS README* doc/*
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%dir %{_includedir}/afflib
%{_includedir}/afflib/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
