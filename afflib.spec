%define	major 0
%define libname	%mklibname afflib %{major}
%define develname %mklibname -d afflib

Summary:	A set of programs for creating and manipulating AFF files
Name:		afflib
Version:	2.3.0
Release:	%mkrel 1
Group:		System/Libraries
License:	BSD
URL:		http://www.afflib.org/
Source0:	http://www.afflib.org/downloads/%{name}-%{version}.tar.gz
Patch0:		afflib-shared.diff
Patch1:		afflib-no_win32.diff
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	curl-devel
BuildRequires:	fuse-devel
BuildRequires:	libewf-devel
BuildRequires:	libexpat-devel
BuildRequires:	libtermcap-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	readline-devel
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
%patch0 -p1
%patch1 -p0

%build
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force; aclocal; autoconf --force; autoheader; automake

export CFLAGS="%{optflags} -fPIC"

%configure2_5x \
    --enable-libewf=yes \
    --enable-s3=yes \
    --enable-fuse=yes \
    --with-curl=%{_prefix}

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

# install headers as well
install -d %{buildroot}%{_includedir}/afflib
install -m0644 lib/*.h %{buildroot}%{_includedir}/afflib/

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/afcat
%{_bindir}/afcompare
%{_bindir}/afconvert
%{_bindir}/afcopy
%{_bindir}/affix
%{_bindir}/affuse
%{_bindir}/afinfo
%{_bindir}/afsegment
%{_bindir}/afstats
%{_bindir}/aftest
%{_bindir}/afxml
%{_bindir}/aimage
%{_bindir}/s3

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS BUGLIST.txt COPYING ChangeLog NEWS README* doc/*
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/afflib
%{_includedir}/afflib/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
