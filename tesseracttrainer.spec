%define	name	tesseracttrainer
%define	version	0.1.3
%define	rel	1
%define	release	%mkrel %{rel}

Summary:	Tesseract Trainer
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://www.mushware.com/files/%{name}-%{version}.tar.bz2
URL:		http://www.mushware.com/
License:	GPL
Group:		Sciences/Mathematics
BuildRequires:	Mesa-common-devel MesaGLU-devel pcre-devel expat-devel
BuildRequires:	ungif-devel tiff-devel SDL-devel SDL_mixer-devel

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

%build
%configure --program-transform-name=""
# App seen to segfault when throwing an exception if omit-frame-pointers is used
%make CXXFLAGS="$RPM_OPT_FLAGS -fno-omit-frame-pointer"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
install -m644 x11/icons/%{name}.16.png -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 x11/icons/%{name}.32.png -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 x11/icons/%{name}.48.png -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/tesseracttrainer
?package(tesseracttrainer):command="tesseracttrainer" \
icon="tesseracttrainer.png" needs="X11" section="More Applications/Games/Toys" \
title="Tesseract Trainer" longtitle="Displays a 4D spinning hypercube"
?package(tesseracttrainer):command="kfmclient exec %{_docdir}/%{name}-%{version}" \
icon="tesseracttrainer.png" needs="X11" section="More Applications/Games/Toys" \
title="Tesseract Trainer Help" longtitle="Documentation for Tesseract Trainer"
EOF

cat << EOF > $RPM_BUILD_ROOT%{_bindir}/tesseracttrainer
#!/bin/sh
cd %{_datadir}/%{name}/system
exec %{_bindir}/tesseracttrainerbinary
EOF
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/tesseracttrainer

cat << EOF > $RPM_BUILD_ROOT%{_bindir}/tesseracttrainer-recover
#!/bin/sh
cd %{_datadir}/%{name}/system
exec %{_bindir}/tesseracttrainerbinary "load('start_safe.txt')"
EOF
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/tesseracttrainer-recover

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README NEWS AUTHORS data-tesseracttrainer/About_Tesseract_Trainer.pdf
%{_datadir}/tesseracttrainer
%{_bindir}/tesseracttrainerbinary
%{_bindir}/tesseracttrainer
%{_bindir}/tesseracttrainer-recover
%{_menudir}/tesseracttrainer
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man6/%{name}*.6*

