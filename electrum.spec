
# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module

%define		egg_name	Electrum
Summary:	Bitcoin Wallet
Summary(pl.UTF-8):	Zarządca portwala Bitcoin
Name:		electrum
Version:	2.9.3
Release:	1
License:	MIT
Group:		Libraries/Python
# Source0:	https://files.pythonhosted.org/packages/source/M/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source0:	https://download.electrum.org/%{version}/Electrum-%{version}.tar.gz
# Source0-md5:	17257d2ee01454283a3324392b85eef5
URL:		https://electrum.org
#URL:		https://pypi.python.org/pypi/MODULE
BuildRequires:	python-PySocks >= 1.6.6
BuildRequires:	python-ecdsa > 0.9
BuildRequires:	python-jsonrpclib
BuildRequires:	python-pbkdf2
BuildRequires:	python-pyaes
BuildRequires:	python-qrcode
BuildRequires:	python-requests
BuildRequires:	python-protobuf
BuildRequires:	python-six
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714

%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
# when using /usr/bin/env or other in-place substitutions
#BuildRequires:	sed >= 4.0
# replace with other requires if defined in setup.py
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lightweight Bitcoin wallet

# %%description -l pl.UTF-8

%package -n python3-%{pypi_name}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{pypi_name}

%description -n python3-%{pypi_name} -l pl.UTF-8

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Pythona %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n Electrum-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

# Fix for strange *.desktop pixmap location rules in setup.py
export XDG_DATA_HOME=%{_datadir}
%if %{with python2}
%py_install
# when files are installed in other way that standard 'setup.py
# they need to be (re-)compiled
# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
#%%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
#%%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS README.rst RELEASE-NOTES
%attr(755,root,root) %{_bindir}/electrum
%{_desktopdir}/electrum.desktop
%{_pixmapsdir}/electrum.png
%{py_sitescriptdir}/electrum
%{py_sitescriptdir}/electrum_gui
%{py_sitescriptdir}/electrum_plugins
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc AUTHORS README.rst RELEASE-NOTES
#%%{py3_sitescriptdir}/%{module}
#%%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
