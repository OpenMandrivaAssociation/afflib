%define	major 0
%define libname	%mklibname afflib %{major}
%define develname %mklibname -d afflib

Summary:	A set of programs for creating and manipulating AFF files
Name:		afflib
Version:	3.3.4
Release:	%mkrel 1
Group:		System/Libraries
License:	BSD
URL:		http://www.afflib.org/
Source0:	http://www.afflib.org/downloads/%{name}-%{version}.tar.gz
#Patch0:		afflib-shared.diff
#Patch1:		afflib-no_win32.diff
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	curl-devel
# GPLv2 FOSS incompatible with BSD with advertising
#BuildRequires:	fuse-devel
BuildRequires:	libewf-devel
BuildRequires:	libexpat-devel
BuildRequires:	libtermcap-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
# GPLv2 FOSS incompatible with BSD with advertising
#BuildRequires:	readline-devel
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
AFFLIB is an open source library developed by Simson Garfinkel and Basis
Technology that implements the AFF standard. AFFLIB is distributed under
4-clause Berkeley License and may be freely incorporated into both Open
Source and Proprietary software.

In addition to the library, AFFLIB also comes with the AFF Tools, a set of
programs for creating and manipulating AFF files.

%package -n	%{libname}
Summary:	A shared library that implements the AFF standard
Group:          System/Libraries

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
#%patch0 -p1
#%patch1 -p0


%build
#export WANT_AUTOCONF_2_5=1
#rm -f configure
#libtoolize --copy --force; aclocal; autoconf --force; autoheader; automake

#TODO fix format not a string literal
%define Werror_cflags %nil

export CFLAGS="%{optflags} -fPIC"

%configure2_5x \
	--enable-shared \
	--enable-wide-character-type \
	--enable-libewf=yes \
    	--enable-s3=yes \
    	--enable-fuse=no \
    	--with-curl=%{_prefix}

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

# install headers as well
install -d %{buildroot}%{_includedir}/afflib
install -m0644 lib/*.h %{buildroot}%{_includedir}/afflib/

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/afcat
%{_bindir}/afcompare
%{_bindir}/afconvert
%{_bindir}/afcopy
%{_bindir}/afcrypto
%{_bindir}/affix
%{_bindir}/affuse
%{_bindir}/afinfo
%{_bindir}/afrecover
%{_bindir}/afsegment
%{_bindir}/afsign
%{_bindir}/afstats
%{_bindir}/aftest
%{_bindir}/afverify
%{_bindir}/afxml
%{_bindir}/s3

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS BUGLIST.txt COPYING ChangeLog NEWS README* doc/*
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/afflib
%{_includedir}/afflib/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
