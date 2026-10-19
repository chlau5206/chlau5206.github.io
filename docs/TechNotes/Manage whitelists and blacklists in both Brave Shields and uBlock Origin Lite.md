1. In Brave Browser (Brave Shields)

Brave makes it very easy to whitelist or blacklist sites directly from the address bar.

How to Whitelist a Site (Allow Popups / Turn Off Blocking)

1. **Navigate** to the specific website you want to allow.
2. Click the orange **Brave Shields icon** (the lion head) at the right end of the address bar.
3. Toggle the big switch at the top to **"Shields are UP"** so it changes to **"Shields are DOWN"**.
4. The page will automatically reload. Popups and ads will now be completely allowed on this specific site while remaining blocked everywhere else.

How to Blacklist a Site (Block Everything Manually)

If you want to create a custom blacklist rule to block a specific site or script:

1. Open Brave’s settings by typing `brave://settings/shields/filters` into your address bar.
2. Scroll down to the bottom to find the **"Create custom filters"** text box.
3. To completely block a specific website, type: `||example.com^` (replace _example.com_ with the site you want to block).
4. Click **Save**.

---

2. In Google Chrome (uBlock Origin Lite)

Because **uBlock Origin Lite** (the version compliant with Google's Manifest V3 rules) is streamlined, whitelisting is done through permission levels.

How to Whitelist a Site (Allow Popups / Turn Off Blocking)

1. **Navigate** to the website where you need popups.
2. Click the extension puzzle piece icon or the **uBlock Origin Lite icon** in your toolbar.
3. You will see a slider showing the current filtering level for that site (Optimal, Complete, etc.).
4. Slide it all the way down to **"No Filtering"** (the gray shield icon).
5. Refresh the page. The extension is now disabled just for this specific domain.

How to Blacklist a Site (Custom Blocking)

Manifest V3 severely restricts how extensions modify lists on the fly, meaning you cannot easily type in custom text-based blocking rules inside uBlock Origin Lite like you could in the old version. If you want to block a site entirely in Chrome, it is best to use Chrome's native tools:

1. Copy the address of the site you want to block.
2. Go to Chrome Settings > **Privacy and security** > **Site settings**.
3. Scroll down, click **Pop-ups and redirects**, and add the URL to the **"Not allowed to send pop-ups or use redirects"** list.

---

==**uBlock Origin gives you the precision to pinpoint and unblock one specific JavaScript file while keeping the rest of the site's ads blocked.

Because this requires advanced "dynamic filtering," Brave Shields is too basic for this task, Adblock Plus cannot do it due to modern extension limits, and **uBlock Origin Lite cannot do it either** (it lacks the advanced dynamic filtering panel). You must use a browser that supports the classic, full-featured **uBlock Origin** (like Firefox or Brave with Shields disabled).

uBlock Origin (Classic)

The full version of uBlock Origin includes a **Live Network Logger** and a **Dynamic Filtering Matrix** designed exactly for this scenario.

Step 1: Turn on Advanced User Mode

1. Click the uBlock Origin icon and open the **Dashboard** (the gears icon).
2. On the _Settings_ tab, check the box next to **"I am an advanced user."** (Click the gears next to it if you want to see advanced settings, but just checking it is enough).

Step 2: Use the Logger to Find and Allow the Script

1. Open the website containing the conversion function.
2. Click the uBlock Origin icon and click the **Open the logger** icon (it looks like a small clipboard/list).
3. Refresh the website page. You will see a live stream of every script loading.
4. Look for rows highlighted in **Red** (these are the blocked scripts). Find the exact JavaScript file containing your conversion function.
5. Hover your mouse over the cell in the **middle column** (the one showing `script`).
6. Click the **Gray block** to set an exception rule, or click the **Green block** to explicitly force it to allow.
7. Click the **Padlock icon** at the top left of the logger or extension popup to save this rule permanently for this site.

---

The Alternative: Brave Shields

Brave Shields **cannot unblock a single specific JS file** while keeping other ads blocked on the same page. Its engine operates on an "all or nothing" approach per script source.

Your only options inside Brave Shields are:

- **Allow all scripts:** Click the Lion icon and toggle "Block Scripts" off (if you had it on), or lower Shields entirely. This lets the conversion script run, but _all_ ads and trackers will load too.
- **Custom Filter Exception:** If you know the exact URL of the script, you can try adding an exception rule in `brave://settings/shields/filters` using an exception modifier: `@@||://example.com`. However, if Brave's built-in blocklist has a broader structural rule blocking that script, local custom rules sometimes fail to override the native Rust engine.

Summary Strategy

If this conversion function is critical for your work, your best setup is to use **Firefox or Brave** (with Brave Shields turned off for this specific site), install the classic **uBlock Origin**, and use the Advanced User Network Logger to green-light that single conversion script.