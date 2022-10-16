# python modules don't need to link -lpython
%define _disable_ld_no_undefined 1

%define	major 0
%define libname		%mklibname %{name}
%define oldlibname	%mklibname %{name} 0
%define develname	%mklibname %{name} -d

%bcond_without	python

Summary:	A set of programs for creating and manipulating AFF files
Name:		afflib
Version:	3.7.19
Release:	1
Group:		System/Libraries
License:	BSD
URL:		https://github.com/sshock/AFFLIBv3
Source0:	https://github.com/sshock/AFFLIBv3/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:		afflib-3.7.19-no-Lusrlib.patch
BuildRequires:	pkgconfig(expat)
# GPLv2 FOSS incompatible with BSD with advertising
#BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(libcurl)
#BuildRequires:	pkgconfig(libedit)
BuildRequires:	pkgconfig(libewf)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(openssl)
# GPLv2 FOSS incompatible with BSD with advertising
#BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(zlib)
%{?_with_python:
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3dist(cython)
#BuildRequires:	python3dist(pip)
BuildRequires:	python3dist(setuptools)
#BuildRequires:	python3dist(wheel)
}

%description
AFFLIB is an open source library developed by Simson Garfinkel and Basis
Technology that implements the AFF standard. AFFLIB is distributed under
4-clause Berkeley License and may be freely incorporated into both Open
Source and Proprietary software.

In addition to the library, AFFLIB also comes with the AFF Tools, a set of
programs for creating and manipulating AFF files.

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
%{_mandir}/man1/aff*.1*

#---------------------------------------------------------------------------

%package -n	%{libname}
Summary:	A shared library that implements the AFF standard
Group:		System/Libraries
%rename %{oldlibname}

%description -n	%{libname}
AFFLIB is an open source library developed by Simson Garfinkel and Basis
Technology that implements the AFF standard. AFFLIB is distributed under
4-clause Berkeley License and may be freely incorporated into both Open
Source and Proprietary software.

This package contains a shared library that implements the AFF standard.

%files -n %{libname}
%doc AUTHORS BUGLIST.txt COPYING ChangeLog NEWS README* doc/*
%{_libdir}/*.so.%{major}*

#---------------------------------------------------------------------------

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

%files -n %{develname}
%dir %{_includedir}/afflib
%{_includedir}/afflib/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

#---------------------------------------------------------------------------

%{?with_python:
%package -n python-pyaff
Summary:        Python3 binding for the AFFLIB
Group:          Development/Libraries

%description -n python-pyaff
Python3 bindings for AFFLIB.
These bindings currently support a read-only file-like interface to AFFLIB and
basic metadata accessor functions. The binding is not currently complete.

%files -n python-pyaff
%license COPYING
%doc pyaff/README
%{py_platsitedir}/pyaff.*.so
%{py_platsitedir}/PyAFF-*-py%{py_ver}.egg-info
}

#---------------------------------------------------------------------------

%prep
%autosetup -p1 -n AFFLIBv3-%{version}

%build
sh bootstrap.sh
%configure \
	--disable-static \
	--enable-shared \
	--enable-wide-character-type \
	--enable-libewf=yes \
	--enable-s3=yes \
	--enable-fuse=no \
	--enable-python=%{?with_python:yes}%{!?with_python:no} \
	--enable-qemu=no \
	--with-curl=yes \
	PYTHON=%{__python3}

%make_build
# Remove rpath from libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
 
# clean unused-direct-shlib-dependencies
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
 
# Remove the cythonized files in order to regenerate them during build.
rm $(grep -rl '/\* Generated by Cython')

%make_build

%{?with_python:
cd pyaff
%global py_setup_args build_ext --include-dirs %{_builddir}/AFFLIBv3-%{version}/include --library-dirs %{_builddir}/AFFLIBv3-%{version}/lib/.libs
%py_build
}

%install
%make_install

%{?with_python:
cd pyaff
%py_install
}
