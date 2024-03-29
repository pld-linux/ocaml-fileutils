#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		_enable_debug_packages	0

Summary:	OCaml functions to manipulate real file (POSIX like) and filename
Summary(pl.UTF-8):	Funkcje OCamla do operacji na (posiksowych) plikach oraz nazwach plików
Name:		ocaml-fileutils
Version:	0.6.3
Release:	2
License:	LGPL v2.1+ with OCaml linking exception
Group:		Libraries
#Source0Download: https://github.com/gildor478/ocaml-fileutils/releases
Source0:	https://github.com/gildor478/ocaml-fileutils/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e6740a32ea1272d54c738d390dab000c
Patch0:		no-stdlib-shims.patch
URL:		https://github.com/gildor478/ocaml-fileutils
BuildRequires:	ocaml >= 1:4.03
BuildRequires:	ocaml-dune >= 1.11.0
BuildRequires:	ocaml-findlib
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
%patch0 -p1

%build
dune build --verbose

%install
rm -rf $RPM_BUILD_ROOT

dune install --destdir=$RPM_BUILD_ROOT

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/fileutils{,/str}/*.ml
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/fileutils

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE.txt README.md
%dir %{_libdir}/ocaml/fileutils
%{_libdir}/ocaml/fileutils/META
%{_libdir}/ocaml/fileutils/fileutils*.cma
%dir %{_libdir}/ocaml/fileutils/str
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/fileutils/fileutils*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/fileutils/str/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/fileutils/dune-package
%{_libdir}/ocaml/fileutils/opam
%{_libdir}/ocaml/fileutils/.private
%{_libdir}/ocaml/fileutils/*.cmi
%{_libdir}/ocaml/fileutils/*.cmt
%{_libdir}/ocaml/fileutils/*.cmti
%{_libdir}/ocaml/fileutils/*.mli
%{_libdir}/ocaml/fileutils/str/*.cmi
%{_libdir}/ocaml/fileutils/str/*.cmt
%{_libdir}/ocaml/fileutils/str/*.cma
%if %{with ocaml_opt}
%{_libdir}/ocaml/fileutils/*.cmx
%{_libdir}/ocaml/fileutils/fileutils*.a
%{_libdir}/ocaml/fileutils/fileutils*.cmxa
%{_libdir}/ocaml/fileutils/str/*.cmx
%{_libdir}/ocaml/fileutils/str/*.a
%{_libdir}/ocaml/fileutils/str/*.cmxa
%endif
