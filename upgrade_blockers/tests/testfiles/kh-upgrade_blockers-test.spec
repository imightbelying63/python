%define name	kh-upgrade_blockers-test
%define version	1.0
%define release	1
Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Test RPM for upgrade_blockers-test.py

Group:		Development/Tools
License:	GPL
BuildArch:	noarch
BuildRoot:	%{_builddir}/%{name}-root
URL:		https://github.com/imightbelying63/python/tree/master/upgrade_blockers

%description
RPM does nothing, it's simply to test the validity of YUM (implying the same for rpm)

%prep
exit 0

%build
exit 0

%install
exit 0

%clean
exit 0

%files
%defattr(-,root,root)

%changelog
* Mon Apr 16 2018 <khughes@liquidweb.com> 0.1
- Initial build
