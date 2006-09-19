%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           PyX
Version:        0.9
Release:        2%{?dist}
Summary:        Python graphics package

Group:          Applications/Publishing
License:        GPL
URL:            http://pyx.sourceforge.net/
Source0:        http://easynews.dl.sourceforge.net/sourceforge/pyx/PyX-%{version}.tar.gz
# Fedora doesn't seem to ship with the python mkhowto script needed to generate
# the manual at build time. The manual here is from:
# http://pyx.sourceforge.net/manual.pdf
Source1:	%{name}-%{version}-manual.pdf
# Fix the install root in the siteconfig.py
Patch0:         PyX-0.8.1-siteconfig.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel >= 2.2
BuildRequires:  tetex-latex
Requires:   tetex

%description
PyX is a Python package for the creation of PostScript and PDF files. It
combines an abstraction of the PostScript drawing model with a TeX/LaTeX
interface. Complex tasks like 2d and 3d plots in publication-ready quality are
built out of these primitives.

%prep
%setup -q
%patch0 -p1


%build
%{__sed} -i 's?^build_t1code=.*?build_t1code=1?' setup.cfg
# Bug #150085 excludes x86_64 - don't enable pykpathsea C module for x86_64
%ifnarch x86_64
%{__sed} -i 's?^build_pykpathsea=.*?build_pykpathsea=1?' setup.cfg
%endif

CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

# turn on ipc in config file
%{__sed} -i 's?^texipc =.*?texipc = 1?' pyxrc

pushd faq
make
popd

pushd manual
## Nope - fedora doesn't ship with mkhowto
## Bug #177349
# ln -s /path/to/python/mkhowto .
# make
cp %{SOURCE1} ./manual.pdf
popd

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Fix the non-exec with shellbang rpmlint errors
for file in `find %{buildroot}%{python_sitearch}/pyx -type f -name "*.py"`; do
  [ ! -x ${file} ] && %{__sed} -i 's?^#!?##?' ${file}
done
 
%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGES LICENSE PKG-INFO README faq/pyxfaq.pdf manual/manual.pdf
%doc contrib/ examples/
%config(noreplace) %{_sysconfdir}/pyxrc
%{_datadir}/pyx/
%dir %{python_sitearch}/pyx
%{python_sitearch}/pyx/*.py
%{python_sitearch}/pyx/*.py[co]
%dir %{python_sitearch}/pyx/graph
%{python_sitearch}/pyx/graph/*.py
%{python_sitearch}/pyx/graph/*.py[co]
%dir %{python_sitearch}/pyx/graph/axis
%{python_sitearch}/pyx/graph/axis/*.py
%{python_sitearch}/pyx/graph/axis/*.py[co]
%dir %{python_sitearch}/pyx/pykpathsea
%{python_sitearch}/pyx/pykpathsea/*.py
%{python_sitearch}/pyx/pykpathsea/*.py[co]
%ifnarch x86_64
%{python_sitearch}/pyx/pykpathsea/*.so
%endif
### t1strip stuff moved to font in 0.9
#%%dir %{python_sitearch}/pyx/t1strip
#%%{python_sitearch}/pyx/t1strip/*.py
#%%{python_sitearch}/pyx/t1strip/*.pyc
#%%ghost %{python_sitearch}/pyx/t1strip/*.pyo
#%%{python_sitearch}/pyx/t1strip/*.so
%dir %{python_sitearch}/pyx/font
%{python_sitearch}/pyx/font/*.py
%{python_sitearch}/pyx/font/*.py[co]
%{python_sitearch}/pyx/font/*.so


%changelog
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
