#
# Conditional build:
%bcond_without	ocaml_opt	# build opt (native code)

%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif
Summary:	OCaml functions to manipulate real file (POSIX like) and filename
Summary(pl.UTF-8):	Funkcje OCamla do operacji na (posiksowych) plikach oraz nazwach plików
Name:		ocaml-fileutils
Version:	0.5.0
Release:	5
License:	LGPL v2.1+ with OCaml linking exception
Group:		Libraries
Source0:	http://forge.ocamlcore.org/frs/download.php/1531/%{name}-%{version}.tar.gz
# Source0-md5:	7d767cdfec85c846bd1d6f75a73abb01
URL:		http://forge.ocamlcore.org/projects/ocaml-fileutils
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-ounit
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Functions to manipulate real file (POSIX like) and filename.

%description -l pl.UTF-8
Funkcje do operacji na (posiksowych) plikach oraz nazwach plików.

%package devel
Summary:	Development files for OCaml fileutils package
Summary(pl.UTF-8):	Pliki programistyczne pakietu fileutils dla OCamla
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains libraries and signature files for developing
applications that use OCaml fileutils package.

%description devel -l pl.UTF-8
Ten pakiet zawiera biblioteki i pliki sygnatur do tworzenia aplikacji
wykorzystujących pakiet OCamla fileutils.

%prep
%setup -q

%build
# note: not autoconf configure
./configure \
	--prefix=%{_prefix} \
	--docdir=$(pwd)/doc \
	--override bytecomp_c_compiler "%{__cc} %{rpmcflags} -D_FILE_OFFSET_BITS=64 -D_REENTRANT -fPIC" \
	--override native_c_compiler "%{__cc} %{rpmcflags} -D_FILE_OFFSET_BITS=64 -D_REENTRANT"

%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{site-lib/fileutils,stublibs}

%{__make} install \
	OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml

mv $RPM_BUILD_ROOT%{_libdir}/ocaml/fileutils/META $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/fileutils
cat >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/fileutils/META <<EOF
directory = "+fileutils"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGELOG.txt README.txt TODO.txt
%dir %{_libdir}/ocaml/fileutils
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/fileutils/fileutils*.cmxs
%endif
%{_libdir}/ocaml/fileutils/fileutils*.cma
%{_libdir}/ocaml/site-lib/fileutils

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/fileutils/*.cmi
%if %{with ocaml_opt}
%{_libdir}/ocaml/fileutils/*.cmx
%{_libdir}/ocaml/fileutils/fileutils*.a
%{_libdir}/ocaml/fileutils/fileutils*.cmxa
%endif
# doc?
%{_libdir}/ocaml/fileutils/FilePath.mli
%{_libdir}/ocaml/fileutils/FileUtil.mli
%{_libdir}/ocaml/fileutils/FileUtil*.ml
