#!/bin/bash

create-dmg \
        --volname "Packer for macOS" \
        --volicon "dmg.icns" \
        --background "dmg.png" \
        --window-pos 200 120 \
        --window-size 750 478 \
        --icon-size 100 \
        --icon "Packer for macOS.app" 376 243 \
        --hide-extension "Packer for macOS.app" \
        "packer-macos.dmg" \
        "../dist/Packer for macOS.app"