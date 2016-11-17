Name:       openstack-clean-all
Version:	1.2
Release:	1%{?dist}
Summary:	Clean openstack resources 

License:	GNU GPL
URL:		https://github.com/vmindru/vmindru-scripts/tree/master/openstack
Source0:    %{name}-%{version}.tar

BuildRequires: python-novaclient python-neutronclient
BuildArch: noarch


%description
Clean openstack resources. 

%prep
%setup -n %{name}-%{version}


%build

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 %{name}.py  %{buildroot}%{_bindir}/%{name}


%files
%{_bindir}/%{name}

%changelog
* Mon Oct 10 2016 Your Name <your@mail.addres>
- Initial Release
