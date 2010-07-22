%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# Necessary as soon as mkhowto is used
# at the moment that is not possible (#220693)
#%define pybasever %(%{__python} -c "from sys import version_info; print '%d.%d' % version_info[:2]")
#%define doc_tools_dir %{_libdir}/python%{pybasever}/Doc/tools

Name:           PyX
Version:        0.10
Release:        9%{?dist}
Summary:        Python graphics package

Group:          Applications/Publishing
License:        GPLv2+
URL:            http://pyx.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sourceforge/pyx/PyX-%{version}.tar.gz
Source1:        %{name}-%{version}-manual.pdf

# Fix the install root in the siteconfig.py
Patch0:         PyX-0.8.1-siteconfig.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  kpathsea-devel
BuildRequires:  tetex-latex
# for mkhowto
#BuildRequires:  python-tools

Requires:       tetex

%description
PyX is a Python package for the creation of PostScript and PDF files. It
combines an abstraction of the PostScript drawing model with a TeX/LaTeX
interface. Complex tasks like 2d and 3d plots in publication-ready quality are
built out of these primitives.

%prep
%setup -q
%patch0 -p1


%build
%{__sed} -i 's|^build_t1code=.*|build_t1code=1|' setup.cfg
%{__sed} -i 's|^build_pykpathsea=.*|build_pykpathsea=1|' setup.cfg

CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

# turn on ipc in config file
%{__sed} -i 's|^texipc =.*|texipc = 1|' pyxrc

# disable for now
# pushd faq
# make
# popd

pushd manual
#ln -s %{doc_tools_dir}/mkhowto .
#make
cp %{SOURCE1} ./manual.pdf
popd

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Fix the non-exec with shellbang rpmlint errors
for file in `find %{buildroot}%{python_sitearch}/pyx -type f -name "*.py"`; do
  [ ! -x ${file} ] && %{__sed} -i 's|^#!|##|' ${file}
done

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES LICENSE PKG-INFO README manual/manual.pdf
%doc contrib/ examples/
%config(noreplace) %{_sysconfdir}/pyxrc
%{_datadir}/pyx/
%{python_sitearch}/pyx/

%if 0%{?fedora} >= 9
%{python_sitearch}/*.egg-info
%endif


%changelog
* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 30 2009 José Matos <jamatos@fc.up.pt> - 0.10-8
- Disable faq pdf generation for now (it breaks the build)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.10-5
- Rebuild for Python 2.6

* Thu Feb 14 2008 José Matos <jamatos[AT]fc.up.pt> - 0.10-4
- Rebuild for gcc 4.3

* Sat Jan 12 2008 José Matos <jamatos[AT]fc.up.pt> - 0.10-3
- egg-info is in sitearch...

* Fri Jan 11 2008 José Matos <jamatos[AT]fc.up.pt> - 0.10-2
- Add egg-info to F9+.

* Fri Jan 11 2008 José Matos <jamatos[AT]fc.up.pt> - 0.10-1
- New upstream release (#426816).
- Package cleanup.

* Tue Aug 28 2007 José Matos <jamatos[AT]fc.up.pt> - 0.9-5
- License fix, rebuild for devel (F8).

* Mon Dec 11 2006 José Matos <jamatos[AT]fc.up.pt> - 0.9-4
- Rebuild for python 2.5.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.9-3
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 José Matos <jamatos[AT]fc.up.pt> - 0.9-2
- Rebuild for FC-6.
- Unghost .pyo files.

* Sat Jun 03 2006 Michael A. Peters <mpeters@mac.com> - 0.9-1
- New upstream release (closes bug #193956)

* Sun Apr 30 2006 Michael A. Peters <mpeters@mac.com> - 0.8.1-4
- Fixed rpmlint errors noted in 190247#3
- Don't build pykpathsea C module for x86_64 (Bug #150085)

* Sat Apr 29 2006 Michael A. Peters <mpeters@mac.com> - 0.8.1-3
- Fixed a typo in the borrowed SuSE patch

* Sat Apr 29 2006 Michael A. Peters <mpeters@mac.com> - 0.8.1-2
- Fix improper siteconfig.py (Patch0, borrowed from SuSE)
- alter default config file (turn texipc on)
- BuildRequires python-devel >= 2.2

* Sat Apr 29 2006 Michael A. Peters <mpeters@mac.com> - 0.8.1-1
- Initial packaging for Fedora Extras
