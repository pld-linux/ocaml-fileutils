Summary:	OCaml functions to manipulate real file (POSIX like) and filename
Summary(pl.UTF-8):	Funkcje OCamla do operacji na (posiksowych) plikach oraz nazwach plików
Name:		ocaml-fileutils
Version:	0.4.4
Release:	1
License:	LGPL v2.1+ with OCaml linking exception
Group:		Libraries
Source0:	http://forge.ocamlcore.org/frs/download.php/892/%{name}-%{version}.tar.gz
# Source0-md5:	1f43b9333358f47660318bfbe9ae68bf
URL:		http://forge.ocamlcore.org/projects/ocaml-fileutils
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-ounit
%requires_eq	ocaml
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Functions to manipulate real file (POSIX like) and filename.

%description -l pl.UTF-8
Funkcje do operacji na (posiksowych) plikach oraz nazwach plików.

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

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/fileutils/File*.mli
# why installed?
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/fileutils/File*.ml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGELOG.txt README.txt TODO.txt src/File*.mli
%dir %{_libdir}/ocaml/fileutils
%{_libdir}/ocaml/fileutils/CommonPath.cmx
%{_libdir}/ocaml/fileutils/ExtensionPath.cmx
%{_libdir}/ocaml/fileutils/FilePath.cm[ix]
%{_libdir}/ocaml/fileutils/FilePath_type.cmx
%{_libdir}/ocaml/fileutils/FileStringExt.cmx
%{_libdir}/ocaml/fileutils/FileUtil.cm[ix]
%{_libdir}/ocaml/fileutils/FileUtilStr.cm[ix]
%{_libdir}/ocaml/fileutils/MacOSPath.cmx
%{_libdir}/ocaml/fileutils/UnixPath.cmx
%{_libdir}/ocaml/fileutils/Win32Path.cmx
%{_libdir}/ocaml/fileutils/fileutils.a
%{_libdir}/ocaml/fileutils/fileutils.cm[ax]*
%{_libdir}/ocaml/fileutils/fileutils-str.a
%{_libdir}/ocaml/fileutils/fileutils-str.cm[ax]*
%{_libdir}/ocaml/site-lib/fileutils
