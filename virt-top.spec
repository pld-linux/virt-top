#
# Conditional build:
%bcond_without	opt		# build opt

%define debug_package %{nil}
Summary:	Utility like top(1) for displaying virtualization stats
Name:		virt-top
Version:	1.0.8
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://people.redhat.com/~rjones/virt-top/files/%{name}-%{version}.tar.gz
# Source0-md5:	cdb61d35e64c78720082d58f8edfb9da
URL:		http://people.redhat.com/~rjones/virt-top/
BuildRequires:	ocaml >= 3.10.2
BuildRequires:	ocaml-findlib-devel
BuildRequires:	ocaml-ocamldoc
ExcludeArch:	sparc64 s390 s390x
# Need the ncurses / ncursesw (--enable-widec) fix.
BuildRequires:	ocaml-calendar-devel
BuildRequires:	ocaml-csv-devel
BuildRequires:	ocaml-curses-devel >= 1.0.3-7
BuildRequires:	ocaml-extlib-devel
#BuildRequires:	ocaml-xml-light-devel # NOT IN PLD
# Need support for virDomainGetCPUStats (fixed in 0.6.1.2).
BuildRequires:	ocaml-libvirt-devel >= 0.6.1.2-5
# Tortuous list of BRs for gettext.
BuildRequires:	ocaml-fileutils-devel
BuildRequires:	ocaml-gettext-tools >= 0.3.3
# For msgfmt:
BuildRequires:	gettext
# Non-OCaml BRs.
BuildRequires:	gawk
BuildRequires:	libvirt-devel
BuildRequires:	perl
BuildRequires:	perl(Pod::Perldoc)
%ifarch ppc ppc64
BuildRequires:	/usr/bin/execstack
%endif

%description
virt-top is a 'top(1)'-like utility for showing stats of virtualized
domains. Many keys and command line options are the same as for
ordinary 'top'.

It uses libvirt so it is capable of showing stats across a variety of
different virtualization systems.

%prep
%setup -q

chmod -x COPYING

%build
%configure
%{__make} all
%if %{with opt}
%{__make} opt
%endif

%if 0
# Build translations.
%{__make} -C po

# Force rebuild of man page.
rm -f virt-top/virt-top.1
%{__make} -C virt-top virt-top.1
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if 0
# Install translations.
install -d $RPM_BUILD_ROOT%{_localedir}
%{__make} -C po install \
	PODIR=$RPM_BUILD_ROOT%{_localedir}
%find_lang %{name}
%endif

# Install virt-top manpage by hand for now.
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p virt-top/virt-top.1 $RPM_BUILD_ROOT%{_mandir}/man1

%ifarch ppc ppc64
# Clear executable stack flag.  Really this is a bug in the OCaml
# compiler on ppc, but it's simpler to just clear the bit here for all
# architectures.
# https://bugzilla.redhat.com/show_bug.cgi?id=605124
# http://caml.inria.fr/mantis/view.php?id=4564
execstack -c $RPM_BUILD_ROOT%{_bindir}/virt-top
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO ChangeLog
%attr(755,root,root) %{_bindir}/virt-top
%{_mandir}/man1/virt-top.1*
