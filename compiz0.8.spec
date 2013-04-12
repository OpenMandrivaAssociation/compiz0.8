%define __noautoreq 'pkgconfig\\(compiz\\)'
%define __noautoprov 'pkgconfig(.*)'

%define oname compiz
%define oversion 0.8
%define git 20130330

%define major 8
%define libname %mklibname decoration %{major}
%define devname %mklibname -d decoration

%if %{git}
%define srcname core-%{oname}-%{oversion}.tar.bz2
%define distname core-%{oname}-%{oversion}
%define rel 0.%{git}.2
%else
%define srcname %{oname}-%{version}.tar.bz2
%define distname %{oname}-%{version}
%define rel 1
%endif


Name:		%{oname}%{oversion}
Version:	0.8.9
Release:	%{rel}
Summary:	OpenGL composite manager for Xgl and AIGLX
Group:		System/X11
License:	GPLv2+ and LGPLv2+ and MIT
URL:		http://www.compiz.org/
Source:		http://cgit.compiz.org/compiz/core/snapshot/%{srcname}
Source1:	compiz.defaults
Source2:	compiz-window-decorator
Source3:	kstylerc.xinit

# (cg) Using git to manage patches
# To recreate the structure
# git clone git://git.freedesktop.org/git/xorg/app/compiz
# git checkout compiz-0.8.0
# git checkout -b mdv-0.8.0-cherry-picks
# git am 00*.patch
# git checkout -b mdv-0.8.0-patches
# git am 05*.patch

# To apply new custom patches
# git checkout mdv-0.8.0-patches
# (do stuff)

# To apply new cherry-picks
# git checkout mdv-0.8.0-cherry-picks
# git cherry-pick <blah>
# git checkout mdv-0.8.0-patches
# git rebase mdv-0.8.0-cherry-picks

# Make sure we don't conflict with main Compiz
Patch0:		compiz0.8-0.8.9-soversion.patch

# Mandriva Patches
# git format-patch --start-number 500 mdv-0.8.0-cherry-picks..mdv-0.8.0-patches
Patch500:	0500-Fix-memory-leak-in-KDE3-window-decorator.patch
Patch501:	0501-Add-Mandriva-graphic-to-the-top-of-the-cube.patch
Patch502:	0502-Use-our-compiz-window-decorator-script-as-the-defaul.patch
Patch503:	0503-Do-not-put-window-decorations-on-KDE-screensaver.patch
Patch504:	0504-Also-check-for-tfp-in-server-extensions.patch
Patch505:	0505-Fix-KDE3-linking-by-changing-the-directory-order.patch

BuildRequires:	x11-util-macros
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(fontconfig)

BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)

BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(zlib)

BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(libwnck-1.0)
BuildRequires:	pkgconfig(libmetacity-private)
BuildRequires:	pkgconfig(pango)

BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(libcanberra-gtk)
BuildRequires:	pkgconfig(libgtop-2.0)

BuildRequires:	kdebase4-devel
BuildRequires:	kdebase4-workspace-devel
BuildRequires:	kdelibs4-devel

BuildRequires:	pkgconfig(libbonoboui-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	libxslt-proc
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(libsvg-cairo)
BuildRequires:	pkgconfig(fuse)
# needed by autoreconf:
BuildRequires:	intltool

Requires(post): GConf2
Requires(preun): GConf2
Requires:	%{libname} = %{version}-%{release}
Requires:	compositing-wm-common
Provides:	compositing-wm%{oversion} = %{version}-%{release}
Requires:	compiz-decorator%{oversion}
Conflicts:	%{oname} > 0.9

%description
Compiz is an OpenGL composite manager for Xgl and AIGLX.

#----------------------------------------------------------------------------

%package decorator-gtk
Summary:	GTK window decorator for compiz
Group:		System/X11
Provides:	compiz-decorator%{oversion} = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{oname}-decorator-gtk

%description decorator-gtk
This package provides a GTK window decorator for the compiz OpenGL
compositing manager.

#----------------------------------------------------------------------------

%package decorator-kde4
Summary:	KDE4 window decorator for compiz
Group:		System/X11
Provides:	compiz-decorator%{oversion} = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{oname}-decorator-kde4

%description decorator-kde4
This package provides a KDE4 window decorator for the compiz OpenGL
compositing manager.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared libraries for compiz
Group:		System/X11

%description -n %{libname}
This package provides shared libraries for compiz.

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for compiz
Group:		Development/X11
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	pkgconfig(gl)
Conflicts:	%{_lib}compiz-devel

%description -n %{devname}
This package provides development files for compiz.

#----------------------------------------------------------------------------

%prep
%setup -q -n %{distname}
%apply_patches

%build
%if %{git}
# This is a CVS snapshot, so we need to generate makefiles.
  sh autogen.sh -V
%else
# (Anssi 03/2008) Needed to get rid of RPATH=/usr/lib64 on lib64:
  autoreconf -i
# build fails without this:
  intltoolize --force
%endif

%configure2_5x \
  --disable-kde \
  --disable-gnome \
  --disable-static \
  --with-default-plugins=core,png,decoration,wobbly,fade,minimize,cube,rotate,zoom,scale,move,resize,place,switcher,screenshot,dbus

%make

%install
%makeinstall_std

install -m755 %{SOURCE2} %{buildroot}%{_bindir}/%{oname}-window-decorator
install -D -m644 %{SOURCE1} %{buildroot}%{_datadir}/compositing-wm/%{oname}.defaults
# Old, unneeded schemas
rm -f %{buildroot}%{_sysconfdir}/gconf/schemas/compiz-kconfig.schemas

%find_lang %{oname}

#----------------------------------------------------------------------------

%files -f %{oname}.lang
%{_bindir}/%{oname}
%{_bindir}/%{oname}-window-decorator
%{_libdir}/%{oname}/lib*.so
%{_sysconfdir}/gconf/schemas/*.schemas
%exclude %{_sysconfdir}/gconf/schemas/gwd.schemas
%dir %{_datadir}/%{oname}
%{_datadir}/%{oname}/*.png
%{_datadir}/%{oname}/*.xml
%{_datadir}/%{oname}/*.xslt
%{_datadir}/compositing-wm/%{oname}.defaults

%files decorator-gtk
%{_bindir}/gtk-window-decorator
%{_sysconfdir}/gconf/schemas/gwd.schemas

%files decorator-kde4
%{_bindir}/kde4-window-decorator

%files -n %{libname}
%{_libdir}/libdecoration.so.%{major}*

%files -n %{devname}
%{_includedir}/%{oname}/%{oname}*.h
%{_includedir}/%{oname}/decoration.h
%{_libdir}/libdecoration.so
%{_libdir}/pkgconfig/%{oname}*.pc
%{_libdir}/pkgconfig/libdecoration.pc

