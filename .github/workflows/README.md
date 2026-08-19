# Workflows

## `download-links.yml`

Verifies every download button on tbn.tbbn.in actually resolves to a real
binary, plus the `latest.yml` auto-update manifest for each product.

Runs daily at 09:00 IST, and on demand from the Actions tab.

### Why this exists

Every download button on the site points at a permanent URL:

```
https://github.com/The-Binary-Brain-Network/<repo>/releases/latest/download/<exact-filename>
```

GitHub resolves that by taking the newest non-draft, non-prerelease release and
asking it for **that exact filename**. There is no fuzzy matching and no
fallback to a similarly-named asset.

That makes the link permanent only for as long as every future release keeps
carrying an asset with that name. It breaks silently if:

- a build job fails but the release publishes anyway, missing one asset
- a release is cut as a draft or prerelease, moving the `latest` pointer
- `artifactName` changes without a release actually producing the new name
- an upload truncates and publishes a partial file

This is not hypothetical. Pass v1.0.6 shipped as `Pass-Setup-1.0.6.exe` while
the site linked to `Pass-Setup.exe`. The `artifactName` had been corrected, but
that only affects future builds — so the permanent URL pointed at a filename
that had never existed. It was fixed by uploading the same verified bytes to
v1.0.6 under the stable name.

**Slate is the larger exposure.** It publishes three assets from separate CI
jobs — `Slate-Setup.exe`, `Slate-Linux.AppImage` and `slate.apk`. If the Linux
or Android job fails while Windows succeeds, the release still publishes and two
of the three buttons on the Slate page go dark with nothing surfacing it.

### What it checks

For each URL: final HTTP status after redirects, `Content-Length` against a
sane floor, and the first four bytes against the expected file signature —
`MZ` for Windows installers, `\x7FELF` for the AppImage, `PK` for the APK.
A status-only check would pass a zero-byte or truncated upload.

`latest.yml` is checked too, and matters more than the buttons: if it is
missing, auto-update is broken for every copy already installed at a customer
site, and nobody finds out until someone complains.

### When it fails

Fix the **release**, not the website. The site links are correct. A failure
means the newest release does not carry an asset with that exact filename.
Either re-upload it to that release under the right name, or cut a new release
that produces it.

---

## Recommended: add a post-release smoke check to each product repo

The nightly check above is the safety net — it catches drift that appears days
after a release, which a release-time check structurally cannot.

A post-release check is the complement: it catches the problem at the moment
it is created, which is the cheapest time to fix it, because you are right
there and the release is fresh in mind.

Add this as the **final job** of the release workflow in each of
`Folio`, `Pass` and `Slate`. Set `FILES` to that product's assets.

```yaml
  verify-download:
    name: Verify published assets resolve
    runs-on: ubuntu-latest
    needs: [build-windows]   # list EVERY build job, so a failed one blocks this
    steps:
      - name: Smoke-check the permanent download URLs
        shell: bash
        env:
          RELEASES_REPO: The-Binary-Brain-Network/pass-releases   # per product
          FILES: "Pass-Setup.exe latest.yml"                      # per product
        run: |
          set -uo pipefail
          # GitHub needs a moment to attach assets and move the latest pointer.
          sleep 30
          FAILED=0
          for f in $FILES; do
            url="https://github.com/$RELEASES_REPO/releases/latest/download/$f"
            code=$(curl -sIL -o /dev/null -w '%{http_code}' --max-time 120 "$url")
            if [ "$code" != "200" ]; then
              echo "::error::$f is not reachable at the permanent URL (HTTP $code)"
              echo "  $url"
              FAILED=$((FAILED+1))
            else
              echo "ok  $f"
            fi
          done
          [ "$FAILED" -eq 0 ] || exit 1
```

Per-product values:

| Repo | `RELEASES_REPO` | `FILES` |
|---|---|---|
| Folio | `The-Binary-Brain-Network/folio-releases` | `Folio-Setup.exe latest.yml` |
| Pass | `The-Binary-Brain-Network/pass-releases` | `Pass-Setup.exe latest.yml` |
| Slate | `The-Binary-Brain-Network/slate-releases` | `Slate-Setup.exe Slate-Linux.AppImage slate.apk latest.yml` |

The `needs:` line matters more than the check itself. Listing every build job
there means a failed Linux or Android build blocks the verification step and
turns the release run red, instead of quietly publishing a release that is
missing an asset.
