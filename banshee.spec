#
%include /usr/lib/rpm/macros.mono
#
Summary:	A Mono/GStreamer Based Music Player
Summary(pl.UTF-8):	Oparty na Mono/GStreamerze odtwarzacz muzyki
Name:		banshee
Version:	2.6.0
Release:	2
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://ftp.gnome.org/pub/GNOME/sources/banshee/2.6/%{name}-%{version}.tar.xz
# Source0-md5:	3b291a0de4c692736b7d8b1b5be038f3
URL:		http://banshee.fm/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.9
BuildRequires:	clutter-devel >= 1.2.0
BuildRequires:	dotnet-dbus-sharp-devel >= 0.7
BuildRequires:	dotnet-dbus-sharp-glib-devel >= 0.5
BuildRequires:	dotnet-gdata-sharp-devel >= 1.5.0
BuildRequires:	dotnet-gio-sharp-devel >= 0.3
BuildRequires:	dotnet-gkeyfile-sharp-devel >= 0.1
BuildRequires:	dotnet-gnome-sharp-devel >= 2.16.0
BuildRequires:	dotnet-gstreamer-sharp-devel
BuildRequires:	dotnet-gtk-sharp-beans-devel >= 2.8
BuildRequires:	dotnet-gtk-sharp2-devel >= 2.12.10
BuildRequires:	dotnet-gudev-sharp-devel >= 0.1
BuildRequires:	dotnet-karma-sharp-devel >= 0.0.5
BuildRequires:	dotnet-libgpod-sharp-devel >= 0.8.2
BuildRequires:	dotnet-mono-upnp-devel >= 0.1
BuildRequires:	dotnet-mono-zeroconf-devel >= 0.8.0
BuildRequires:	dotnet-notify-sharp-devel
BuildRequires:	dotnet-taglib-sharp-devel >= 2.0.3.7
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.22.0
BuildRequires:	gnome-desktop2-devel
BuildRequires:	gnome-doc-utils >= 0.18.0
BuildRequires:	gstreamer0.10-devel >= 0.10.26
BuildRequires:	gstreamer0.10-plugins-base-devel >= 0.10.26
BuildRequires:	gtk+2-devel >= 2:2.22.0
BuildRequires:	gtk-webkit-devel >= 1.2.2
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libmtp-devel >= 0.3.0
BuildRequires:	libsoup-gnome-devel >= 2.26.0
BuildRequires:	libtool
BuildRequires:	mono-addins-devel >= 0.6.2
BuildRequires:	mono-csharp >= 2.4.3
BuildRequires:	monodoc
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sqlite3-devel >= 3.4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libXrandr-devel >= 1.1.1
BuildRequires:	xorg-lib-libXxf86vm-devel >= 1.0.1
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	shared-mime-info
Requires:	gstreamer0.10-GConf >= 0.10.26
Requires:	gstreamer0.10-cdparanoia >= 0.10.26
Requires:	hicolor-icon-theme
Requires:	mono-addins >= 0.6.2
Suggests:	brasero
Suggests:	media-player-info
Obsoletes:	banshee-official-plugins <= 0.11.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Banshee is a brand spankin' new audio player based on the GStreamer
media library and is developed on the Open Source Mono .NET Platform,
written in C#.

%description -l pl.UTF-8
Banshee to nowy odtwarzacz dźwięku oparty na bibliotece odtwarzacza
multimediów GStreamer, rozwijany na platformie .NET Mono, napisany w
C#.

%package devel
Summary:	Banshee development files
Summary(pl.UTF-8):	Pliki programistyczne dla Banshee
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dotnet-dbus-sharp-devel >= 0.7
Requires:	dotnet-dbus-sharp-glib-devel >= 0.5
Requires:	dotnet-gtk-sharp2-devel >= 2.12.10
Requires:	dotnet-taglib-sharp-devel >= 2.0.3.7
Requires:	mono-addins-devel >= 0.6.2

%description devel
This package provides development files for Banshee.

%description devel -l pl.UTF-8
Ten pakiet dostarcza pliki programistyczne dla Banshee.

%prep
%setup -q

%build
%{__libtoolize}
%{__intltoolize}
%{__aclocal} -I build/m4/banshee -I build/m4/shave -I build/m4/shamrock
%{__automake}
%{__autoconf}

%configure \
	--disable-boo \
	--disable-docs \
	--disable-shave \
	--with-vendor-build-id="%{distribution}"
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/*.{la,a}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/Backends/*.{la,a}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_icon_cache hicolor
%update_mime_database

%postun
%update_desktop_database_postun
%update_icon_cache hicolor
%update_mime_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/banshee
%attr(755,root,root) %{_bindir}/bamz
%attr(755,root,root) %{_bindir}/muinshee
%{_datadir}/banshee
%dir %{_libdir}/banshee
%{_libdir}/banshee/*.dll
%attr(755,root,root) %{_libdir}/banshee/*.so
%{_libdir}/banshee/*.exe
%{_libdir}/banshee/*.mdb
%{_libdir}/banshee/*.config
%dir %{_libdir}/banshee/Extensions
%{_libdir}/banshee/Extensions/*.dll
%{_libdir}/banshee/Extensions/*.exe
%{_libdir}/banshee/Extensions/*.mdb
%{_libdir}/banshee/Extensions/Banshee.NotificationArea.dll.config
%{_libdir}/banshee/Extensions/karma-sharp.dll.config
%{_libdir}/banshee/Extensions/libgpod-sharp.dll.config
%dir %{_libdir}/banshee/Backends
%{_libdir}/banshee/Backends/*.config
%{_libdir}/banshee/Backends/*.dll
%{_libdir}/banshee/Backends/*.mdb
%{_libdir}/banshee/Backends/*.so
%{_libdir}/banshee/Banshee.Services.addins
%{_desktopdir}/banshee-audiocd.desktop
%{_desktopdir}/banshee-media-player.desktop
%{_desktopdir}/banshee.desktop
%{_iconsdir}/hicolor/*/*/*
%{_datadir}/dbus-1/services/org.bansheeproject.Banshee.service
%{_datadir}/dbus-1/services/org.bansheeproject.CollectionIndexer.service
%{_datadir}/mime/packages/banshee-amz.xml
%{_datadir}/mime/packages/banshee-emx.xml

%files devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/banshee*.pc
