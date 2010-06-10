#
%include /usr/lib/rpm/macros.mono
#
Summary:	A Mono/GStreamer Based Music Player
Summary(pl.UTF-8):	Oparty na Mono/GStreamerze odtwarzacz muzyki
Name:		banshee
Version:	1.6.1
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://download.banshee-project.org/banshee/%{name}-1-%{version}.tar.bz2
# Source0-md5:	c3456dfa052d9a323f68d3763212c23d
URL:		http://banshee-project.org/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.9
BuildRequires:	brasero-devel >= 2.28.0
BuildRequires:	clutter-devel >= 1.0.1
BuildRequires:	dbus-devel >= 0.93
BuildRequires:	dbus-glib-devel >= 0.71
BuildRequires:	dotnet-gdata-sharp-devel
BuildRequires:	dotnet-gnome-sharp-devel >= 2.16.0
BuildRequires:	dotnet-gtk-sharp2-devel >= 2.12.0
BuildRequires:	dotnet-ipod-sharp-devel >= 0.8.5
BuildRequires:	dotnet-libgphoto2-sharp-devel
BuildRequires:	dotnet-mono-zeroconf-devel >= 0.7.3
BuildRequires:	dotnet-ndesk-dbus-glib-sharp-devel >= 0.3
BuildRequires:	dotnet-njb-sharp
BuildRequires:	dotnet-notify-sharp-devel
BuildRequires:	dotnet-taglib-sharp-devel >= 2.0.3.7
BuildRequires:	dotnet-webkit-sharp-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-desktop-devel >= 2.16.0
BuildRequires:	gstreamer-GConf >= 0.10.3
BuildRequires:	gstreamer-cdparanoia
BuildRequires:	gstreamer-devel >= 0.10.12
BuildRequires:	gstreamer-gnomevfs
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.25.2
BuildRequires:	gtk+2-devel >= 2:2.10.3
BuildRequires:	hal-devel >= 0.5.2
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libmtp-devel >= 0.2.0
BuildRequires:	libmusicbrainz-devel >= 2.1.1
BuildRequires:	libtool
BuildRequires:	mono-addins-devel >= 0.3.1-2
BuildRequires:	mono-csharp >= 2.4.3
BuildRequires:	monodoc
BuildRequires:	pkgconfig
BuildRequires:	sqlite3-devel >= 3.4.0
Requires:	dotnet-ipod-sharp >= 0.8.5
Requires:	gstreamer-GConf >= 0.10.3
Requires:	gstreamer-cdparanoia >= 0.10.3
Requires:	gstreamer-gnomevfs >= 0.10.3
Requires:	mono-addins >= 0.3.1-2
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

%prep
%setup -q -n %{name}-1-%{version}

%build
%{__libtoolize}
%{__intltoolize}
%{__aclocal} -I build/m4/banshee -I build/m4/shave -I build/m4/shamrock
%{__automake}
%{__autoconf}

bash %configure \
	--disable-boo \
	--enable-ipod \
	--disable-docs \
	--disable-shave \
	--with-vendor-build-id="%{distribution}"
%{__make} -j1 \
	SHELL=/bin/bash

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/monodoc/sources

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#mv $RPM_BUILD_ROOT%{_docdir}/%{name}/* $RPM_BUILD_ROOT%{_libdir}/monodoc/sources

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}-1/*.{la,a}
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}-1/Backends/*.{la,a}
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}-1/gstreamer-0.10/*.{la,a}

%find_lang %{name}-1

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_icon_cache hicolor

%postun
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f %{name}-1.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/banshee-1
%attr(755,root,root) %{_bindir}/muinshee
%{_datadir}/banshee-1
%{_pkgconfigdir}/banshee-1*.pc
%dir %{_libdir}/banshee-1
%{_libdir}/banshee-1/*.dll
%attr(755,root,root) %{_libdir}/banshee-1/*.so
%{_libdir}/banshee-1/*.exe
%{_libdir}/banshee-1/*.mdb
%{_libdir}/banshee-1/*.config
%dir %{_libdir}/banshee-1/Extensions
%{_libdir}/banshee-1/Extensions/*.dll
%{_libdir}/banshee-1/Extensions/*.mdb
%{_libdir}/banshee-1/Extensions/Banshee.NotificationArea.dll.config
%dir %{_libdir}/banshee-1/Backends
%{_libdir}/banshee-1/Backends/*.config
%{_libdir}/banshee-1/Backends/*.dll
%{_libdir}/banshee-1/Backends/*.mdb
%{_libdir}/banshee-1/Backends/*.so
%{_libdir}/banshee-1/Banshee.Services.addins
%dir %{_libdir}/banshee-1/gstreamer-0.10
%{_libdir}/banshee-1/gstreamer-0.10/*.so
#%{_libdir}/banshee-1/libbanshee.a
#%{_libdir}/banshee-1/libbanshee.la
#%{_libdir}/monodoc/sources/*
%{_desktopdir}/banshee-1-audiocd.desktop
%{_desktopdir}/banshee-1-media-player.desktop
%{_desktopdir}/banshee-1.desktop
%{_iconsdir}/hicolor/*/*/*
%{_datadir}/dbus-1/services/org.bansheeproject.Banshee.service
%{_datadir}/dbus-1/services/org.bansheeproject.CollectionIndexer.service
