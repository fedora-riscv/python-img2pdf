%global         srcname  img2pdf
%global         desc   Python 3 library and command line utility img2pdf for losslessly converting\
a bunch of image files into a PDF file. That means that the images\
are either inserted into the PDF as-is or they are recompressed using\
lossless compression. Thus, img2pdf usually runs faster and may yield\
smaller PDF files than an ImageMagick convert command.\
\
The img2pdf command complements the pdfimages command.

Name:           python-%{srcname}
Version:        0.4.3
Release:        1%{?dist}
Summary:        Lossless images to PDF conversion library and command

License:        LGPLv3+
URL:            https://pypi.org/project/img2pdf
Source0:        %pypi_source


BuildArch:      noarch

# cf. Bug 1851638 - img2pdf fails to build on s390x because of issues in the ImageMagick dependency
# https://bugzilla.redhat.com/show_bug.cgi?id=1851638
ExcludeArch:    s390x

# Disable tests on EPEL8 for now, since some of the dependencies aren't available
%if 0%{?epel} == 0
# required for tests
BuildRequires:  python3-pytest
BuildRequires:  ImageMagick
BuildRequires:  ghostscript
BuildRequires:  libtiff-tools
BuildRequires:  mupdf
BuildRequires:  netpbm-progs
BuildRequires:  perl-Image-ExifTool
BuildRequires:  poppler-utils
BuildRequires:  python3-numpy
BuildRequires:  python3-scipy
%endif

# other requirements
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools


%if 0%{?epel} == 0
BuildRequires:  python3-pillow
BuildRequires:  python3-pikepdf
%endif


# The Python dependency generator is enabled by default since f30 or so.
# It adds `Requires:` for:
#
# pikepdf
# pillow

%description
%{desc}

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}

%prep
%autosetup -p1 -n %{srcname}-%{version}

# disable in EPEL builds since pikepdf isn't available on CentOS 8/EPEL
# (img2pdf then falls back to its internal PDF engine)
#
# alternatively, we could disable the python dependency generator, however as of 2020-12
# the necessary disable macro isn't available in the epel8 build environment
# cf. https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/SI5CXXV3MWMEH3PLKAVAJK22FRNI7OGM/
%if 0%{?epel} != 0
sed -i '/^INSTALL_REQUIRES/,/)/s/\("pikepdf".*$\)/### not available on EPEL ### \1/' setup.py
%endif


%build
sed -i '1{/^#!\//d}' src/*.py
%py3_build

%install
%py3_install

%check

%if 0%{?epel} == 0

# since the test directly calls src/img2pdf.py
# (file is already installed at this point)
sed -i '1i#!'%{__python3} src/img2pdf.py


PYTHONPATH=src %{__python3} -m pytest src/img2pdf_test.py -v

%endif

%files -n python3-%{srcname}
%{_bindir}/%{srcname}
%{_bindir}/%{srcname}-gui
%{python3_sitelib}/%{srcname}.py
%{python3_sitelib}/jp2.py
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{srcname}-%{version}*.egg-info
%doc README.md


%changelog
* Sat Oct 30 2021 Georg Sauthoff <mail@gms.tf> - 0.4.3-1
- Update to latest upstream version (fixes fedora#2016838)

* Sat Oct 16 2021 Georg Sauthoff <mail@gms.tf> - 0.4.2-1
- Update to latest upstream version (fixes fedora#2012933)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 04 2021 Georg Sauthoff <mail@gms.tf> - 0.4.1-1
- Update to latest upstream version (fixes fedora#1958668)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.4.0-6
- Rebuilt for Python 3.10

* Fri Apr 23 2021 Georg Sauthoff <mail@gms.tf> - 0.4.0-5
- Disable fragile test cases for Python 3.10 (fixes fedora#1949003)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Dec 27 2020 Georg Sauthoff <mail@gms.tf> - 0.4.0-3
- Support EPEL8 - fix macro expansion

* Sat Dec 19 2020 Georg Sauthoff <mail@gms.tf> - 0.4.0-2
- Support EPEL8 (fixes fedora#1907226)

* Sun Sep 20 2020 Georg Sauthoff <mail@gms.tf> - 0.4.0-1
- Update to latest upstream version (fixes fedora#1867007)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 29 2020 Georg Sauthoff <mail@gms.tf> - 0.3.4-5
- Temporarily disable some tests until next release fixes them.

* Fri Jun 26 2020 Georg Sauthoff <mail@gms.tf> - 0.3.4-4
- Be more explicit regarding setuptools depenency,
  cf. https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/GCPGM34ZGEOVUHSBGZTRYR5XKHTIJ3T7/

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.4-3
- Rebuilt for Python 3.9

* Thu Apr 30 2020 Georg Sauthoff <mail@gms.tf> - 0.3.4-2
- Add upstream fix for test suite failure on aarch64

* Sun Apr 26 2020 Georg Sauthoff <mail@gms.tf> - 0.3.4-1
- Update to latest upstream version

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 15 2018 Georg Sauthoff <mail@gms.tf> - 0.3.2-2
- Fix unittest false-negatives on aarch64
* Sat Nov 24 2018 Georg Sauthoff <mail@gms.tf> - 0.3.2-1
- Update to latest upstream version
* Sat Aug 11 2018 Georg Sauthoff <mail@gms.tf> - 0.3.1-1
- Update to latest upstream version
* Wed Aug 1 2018 Georg Sauthoff <mail@gms.tf> - 0.3.0-1
- Update to latest upstream version
* Tue May 1 2018 Georg Sauthoff <mail@gms.tf> - 0.2.4-1
- initial packaging
