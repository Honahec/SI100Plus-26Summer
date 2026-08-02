{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "aarch64-darwin"
        "x86_64-linux"
      ];
      perSystem =
        { pkgs, ... }:
        let
          nodeEnv = with pkgs; [
            git
            nodejs
            pnpm
          ];
        in
        {
          formatter = pkgs.nixpkgs-fmt;
          devShells.default = pkgs.mkShellNoCC {
            packages = nodeEnv;
            shellHook = pkgs.lib.optionalString pkgs.stdenv.isDarwin ''
              unset DEVELOPER_DIR SDKROOT
            '';
          };
          packages.default = pkgs.stdenv.mkDerivation (finalAttrs: {
            name = "si100-static-page";
            pname = "si100-static-page";
            version = "0.1.0";
            src = ./.;

            nativeBuildInputs = [
              nodeEnv
              pkgs.pnpm.configHook
            ];

            pnpmDeps = pkgs.pnpm.fetchDeps {
              inherit (finalAttrs) pname version src;
              fetcherVersion = 1;
              hash = "sha256-CO2L8w3649XTaEvPgcZeNlUTPz7+on/wbx21xYd3zH4=";
            };

            buildPhase =
              ''
                runHook preBuild
                mkdir -p ./static
                find slides/ -name '*.md' \
                  ! -exec grep -q 'marp: true' {} \; \
                  -print | sort | while read -r file; do
                  
                  filename=$(basename "$file" .md)
                  output_dir="static/$filename"
                  echo "Processing $output_dir"

                  pnpm exec reveal-md $file --static $output_dir --template ./assets/reveal.html --preprocessor ./assets/preproc.js --scripts assets/menu/menu.js,assets/inject.js
                  mkdir -p $output_dir/_assets/assets/menu
                  cp assets/menu/menu.css $output_dir/_assets/assets/menu/menu.css
                  file_dir=$(dirname $file)
                  if [ -d "$file_dir/images" ]; then
                    cp -r $file_dir/images $output_dir
                  fi
                done

                printf '%s\n' '<ul class="slide-menu-items">' > static/lectures.html
                find static -mindepth 1 -maxdepth 1 -type d -name 'Lecture_*' -print | sort | while read -r lecture; do
                  slug=$(basename "$lecture")
                  title=$(printf '%s' "$slug" | tr '_' ' ')
                  printf '<li class="slide-menu-item"><a href="../%s/">%s</a></li>\n' "$slug" "$title" >> static/lectures.html
                done
                printf '%s\n' '</ul>' >> static/lectures.html
                runHook postBuild
              '';

            installPhase = ''
              runHook preInstall
              mkdir -p $out
              cp -r static/* $out
              runHook postInstall
            '';
          });
        };
    };
}
