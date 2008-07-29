Summary:	Tesseract Trainer
Name:		tesseracttrainer
Version:	0.1.4
Release:	%mkrel 3
Source0:	http://www.mushware.com/files/%{name}-%{version}.tar.gz
Patch0:		tesseracttrainer-0.1.4-build.patch
URL:		http://www.mushware.com/
License:	GPLv2
Group:		Sciences/Mathematics
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	Mesa-common-devel
BuildRequires:	MesaGLU-devel
BuildRequires:	pcre-devel
BuildRequires:	expat-devel
BuildRequires:	ungif-devel
BuildRequires:	tiff-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_mixer-devel

%description
Tesseract Trainer generates a full screen real time display of a rotating
tesseract - the equivalent of the cube in 4 dimensions. This app also adds
point textures, which give you a feel of what each of the eight faces are
doing. There's a stereoscopic option which adds 3D depth to the projection
from 4D, music and numerous options to play with. I'm very keen to get
feedback as to whether anyone can 'see' the 4D effect here.

The application contains a number of interesting features.  Point textures
convey the orientation of each of the faces as the hypercube rotates.  The
two invariant planes of the rotation are shown.  Any number of faces can be
drawn, so each can be followed in turn.  The facets of each face can be
textured, and faces on each axis are shown in different colours to distinguish
them.  A manual is provided in PDF format, together with key control help
whilst the application is running.  Display resolution can be selected to
match the display.  Finally, some experimental seven-time music creates a bit
of atmosphere.

%prep
%setup -q
%patch0 -p1

%build
%configure --program-transform-name=""
# App seen to segfault when throwing an exception if omit-frame-pointers is used
%make CXXFLAGS="$RPM_OPT_FLAGS -fno-omit-frame-pointer"

%install
rm -rf %{buildroot}
%makeinstall
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m644 x11/icons/%{name}.16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 x11/icons/%{name}.32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 x11/icons/%{name}.48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=Tesseract Trainer
Comment=Displays a 4D spinning hypercube
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Education;Science;Math;Physics;Amusement;
EOF

cat << EOF > %{buildroot}%{_bindir}/tesseracttrainer
#!/bin/sh
cd %{_datadir}/%{name}/system
exec %{_bindir}/tesseracttrainerbinary
EOF
chmod 0755 %{buildroot}%{_bindir}/tesseracttrainer

cat << EOF > %{buildroot}%{_bindir}/tesseracttrainer-recover
#!/bin/sh
cd %{_datadir}/%{name}/system
exec %{_bindir}/tesseracttrainerbinary "load('start_safe.txt')"
EOF
chmod 0755 %{buildroot}%{_bindir}/tesseracttrainer-recover

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README NEWS COPYING AUTHORS data-tesseracttrainer/About_Tesseract_Trainer.pdf
%{_datadir}/tesseracttrainer
%{_bindir}/tesseracttrainerbinary
%{_bindir}/tesseracttrainer
%{_bindir}/tesseracttrainer-recover
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man6/%{name}*.6*

