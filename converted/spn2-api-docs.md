[]{#anchor} Save Page Now 2 Public API Docs Draft

Vangelis Banos, updated: 2025-10-22

Capture a web page as it appears now for use as a trusted citation in
the future. Changelog:
[*https://docs.google.com/document/d/19RJsRncGUw2qHqGGg9lqYZYf7KKXMDL1Mro5o1Qw6QI/edit#*](https://docs.google.com/document/d/19RJsRncGUw2qHqGGg9lqYZYf7KKXMDL1Mro5o1Qw6QI/edit#)

Contents

[]{#anchor-1}Glossary

|           |                                                                                                                                                                                                       |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Capture   | A record in the Wayback Machine that can be accessed like this: [*http://web.archive.org/web/20051231203615/http://www.bbc.co.uk/*](http://web.archive.org/web/20051231203615/http://www.bbc.co.uk/)  |
| Timestamp | A datetime format used in the Wayback Machine: YYYYMMDDHHMMSS. Example: 20051231203615                                                                                                                |
| Embeds    | Components of a web page, e.g. images, CSS, JS, etc. When we capture a web page, we also try to capture its embeds. We return them with the capture result.                                           |
| Outlinks  | Links found inside the capture. We return them with the capture result.                                                                                                                               |

[]{#anchor-2}Basic API Reference

The Save Page Now 2 (SPN2) API enables you to make a **capture request**
and then check its progress with a **status request**.

[]{#anchor-3}Capture request

SPN2 runs on
[*https://web.archive.org/save*](https://web.archive.org/save) which
requires authentication using two alternative methods:

1.  **S3 API Keys** (highly preferable). Get your account's keys at
    > [*https://archive.org/account/s3.php*](https://archive.org/account/s3.php)
    > Use HTTP Header *\"**authorization: LOW myaccesskey:mysecret**\"*
    > in your requests.

2.  Cookies: Get **logged-in-sig** and **logged-in-user** from your
    > browser when you log in to
    > [*https://archive.org*](https://archive.org) and add them to your
    > SPN2 HTTP requests. Cookies are not desirable because they tend to
    > expire after a few days so you would need to login again to
    > archive.org to get new cookies.

To capture a web page via the API, you can use an HTTP POST or GET
request as follows:

<table>
<tbody>
<tr class="odd">
<td><p>curl -X POST -H "Accept: application/json" -H "Authorization: LOW
myaccesskey:mysecret" -d'url=<a
href="http://brewster.kahle.org/"><em>http://brewster.kahle.org/</em></a>'
<a
href="https://web.archive.org/save"><em>https://web.archive.org/save</em></a></p>
<p>or</p>
<p>curl -X GET -H "Accept: application/json" --cookie
"logged-in-sig=xxx;logged-in-user=user1%40archive.org;"
https://web.archive.org/save/http://brewster.kahle.org/</p></td>
</tr>
</tbody>
</table>

**Additional capture request options (HTTP POST required)**.

**Important note: **Anything other than \"1\" or \"on\" is considered to
be \"off\". If you use \"01\" or \"True\" it means \"off\".

<table>
<tbody>
<tr class="odd">
<td><strong>Parameter</strong></td>
<td><strong>Description</strong></td>
</tr>
<tr class="even">
<td>capture_all=1</td>
<td>Capture a web page with errors (HTTP status=4xx or 5xx). By default
SPN2 captures only status=200 URLs.</td>
</tr>
<tr class="odd">
<td>capture_outlinks=1</td>
<td>Capture web page outlinks automatically. This also applies to PDF,
JSON, RSS and MRSS feeds.</td>
</tr>
<tr class="even">
<td>capture_screenshot=1</td>
<td>Capture full page screenshot in PNG format. This is also stored in
the Wayback Machine as a different capture.</td>
</tr>
<tr class="odd">
<td>delay_wb_availability=1</td>
<td>The capture becomes available in the Wayback Machine after ~12 hours
instead of immediately. This option helps reduce the load on our
systems. All API responses remain exactly the same when using this
option.</td>
</tr>
<tr class="even">
<td>force_get=1</td>
<td>Force the use of a simple HTTP GET request to capture the target
URL. By default SPN2 does a HTTP HEAD on the target URL to decide
whether to use a headless browser or a simple HTTP GET request.
force_get overrides this behavior.</td>
</tr>
<tr class="odd">
<td>skip_first_archive=1</td>
<td>Skip checking if a capture is a first if you don’t need this
information. This will make captures run faster.</td>
</tr>
<tr class="even">
<td>if_not_archived_within=&lt;timedelta&gt;</td>
<td>Capture web page only if the latest existing capture at the Archive
is older than the &lt;timedelta&gt; limit<strong>. </strong>Its format
could be any datetime expression like "3d 5h 20m" or just a number of
seconds, e.g. "120". If there is a capture within the defined timedelta,
SPN2 returns that as a recent capture. The default system
&lt;timedelta&gt; is 45 min.</td>
</tr>
<tr class="odd">
<td><p>if_not_archived_within=</p>
<p>&lt;timedelta1&gt;,&lt;timedelta2&gt;</p></td>
<td>When using 2 comma separated &lt;timedelta&gt; values, the first one
applies to the main capture and the second one applies to outlinks.</td>
</tr>
<tr class="even">
<td>outlinks_availability=1</td>
<td>Return the timestamp of the last capture for all outlinks.</td>
</tr>
<tr class="odd">
<td>email_result=1</td>
<td>Send an email report of the captured URLs to the user’s email.</td>
</tr>
<tr class="even">
<td>js_behavior_timeout=&lt;N&gt;</td>
<td><p>Run JS code for &lt;N&gt; seconds after page load to trigger
target page functionality like image loading on mouse over, scroll down
to load more content, etc. The default system &lt;N&gt; is 5 sec.</p>
<p>More details on the JS code we execute:</p>
<p><a
href="https://github.com/internetarchive/brozzler/blob/master/brozzler/behaviors.yaml"><em>https://github.com/internetarchive/brozzler/blob/master/brozzler/behaviors.yaml</em></a></p>
<p>WARNING: The max &lt;N&gt; value that applies is 30 sec.</p>
<p>NOTE: If the target page doesn’t have any JS you need to run, you can
use js_behavior_timeout=0 to speed up the capture.</p></td>
</tr>
<tr class="odd">
<td>capture_cookie=&lt;XXX&gt;</td>
<td>Use extra HTTP Cookie value when capturing the target page.</td>
</tr>
<tr class="even">
<td>use_user_agent=&lt;XXX&gt;</td>
<td>Use custom HTTP User-Agent value when capturing the target page.
</td>
</tr>
<tr class="odd">
<td><p>target_username=&lt;XXX&gt;</p>
<p>target_password=&lt;YYY&gt;</p></td>
<td>Use your own username and password in the target page’s login
forms.</td>
</tr>
</tbody>
</table>

Example

|                                                                                                                                                                                                                                                |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| curl -X POST -H \"Accept: application/json\" -d\'url=http://brewster.kahle.org/&capture_outlinks=1&capture_all=1\' -H \"Authorization: LOW myaccesskey:mysecret\" [*https://web.archive.org/save*](http://vbanos-dev.us.archive.org:8092/save) |

In any case, a capture request might return:

|                                                                                                                               |
|-------------------------------------------------------------------------------------------------------------------------------|
| {\"url\":\"[*http://brewster.kahle.org/*](http://brewster.kahle.org/)\", \"job_id\":\"ac58789b-f3ca-48d0-9ea6-1d1225e98695\"} |

[]{#anchor-4}Status request

It is possible to see the status of one or multiple captures via the
API.

To see a capture status, you can use an HTTP GET or POST request as
follows:

<table>
<tbody>
<tr class="odd">
<td><p>curl -X GET -H "Accept: application/json" -H "Authorization: LOW
myaccesskey:mysecret" <a
href="https://web.archive.org/save/status/ac58789b-f3ca-48d0-9ea6-1d1225e98695"><em>https://web.archive.org/save/status/ac58789b-f3ca-48d0-9ea6-1d1225e98695</em></a></p>
<p>or</p>
<p>curl -X POST -H "Accept: application/json"
-d'job_id=ac58789b-f3ca-48d0-9ea6-1d1225e98695' --cookie
"logged-in-sig=AAAAAAAAAA;logged-in-user=user1%40archive.org;" <a
href="https://web.archive.org/save/status"><em>https://web.archive.org/save/status</em></a></p></td>
</tr>
</tbody>
</table>

In any case, a capture status request might return the following if
successful:

<table>
<tbody>
<tr class="odd">
<td><p> {"status":"success",<br />
"job_id":"ac58789b-f3ca-48d0-9ea6-1d1225e98695",<br />
"original_url":"<a
href="http://brewster.kahle.org/"><em>http://brewster.kahle.org/</em></a>",</p>
<p>
"screenshot":"http://web.archive.org/screenshot/http://brewster.kahle.org/"<br />
"timestamp":"20180326070330",<br />
"duration_sec":6.203,<br />
"resources":[<br />
"http://brewster.kahle.org/",<br />
"http://brewster.kahle.org/favicon.ico",<br />
"http://brewster.kahle.org/files/2011/07/bkheader-follow.jpg",<br />
"http://brewster.kahle.org/files/2016/12/amazon-unhappy.jpg",<br />
"http://brewster.kahle.org/files/2017/01/computer-1294045_960_720-300x300.png",<br />
"http://brewster.kahle.org/files/2017/11/20thcenturytimemachineimages_0000.jpg",<br />
"http://brewster.kahle.org/files/2018/02/IMG_6041-1-300x225.jpg",<br />
"http://brewster.kahle.org/files/2018/02/IMG_6061-768x1024.jpg",<br />
"http://brewster.kahle.org/files/2018/02/IMG_6103-300x225.jpg",<br />
"http://brewster.kahle.org/files/2018/02/IMG_6132-225x300.jpg",<br />
"http://brewster.kahle.org/files/2018/02/IMG_6138-1-300x225.jpg",<br />
"http://brewster.kahle.org/wp-content/themes/twentyten/images/wordpress.png",<br />
"http://brewster.kahle.org/wp-content/themes/twentyten/style.css",<br />
"http://brewster.kahle.org/wp-includes/js/wp-embed.min.js?ver=4.9.4",<br />
"http://brewster.kahle.org/wp-includes/js/wp-emoji-release.min.js?ver=4.9.4",<br />
"http://platform.twitter.com/widgets.js",<br />
"https://archive-it.org/piwik.js",<br />
"https://platform.twitter.com/jot.html",<br />
"https://platform.twitter.com/js/button.556f0ea0e4da4e66cfdc182016dbd6db.js",<br />
"https://platform.twitter.com/widgets/follow_button.f47a2e0b4471326b6fa0f163bda46011.en.html",<br />
"https://syndication.twitter.com/settings",<br />
"https://www.syndikat.org/en/joint_venture/embed/",<br />
"https://www.syndikat.org/wp-admin/images/w-logo-blue.png",<br />
"https://www.syndikat.org/wp-content/plugins/user-access-manager/css/uamAdmin.css?ver=1.0",<br />
"https://www.syndikat.org/wp-content/plugins/user-access-manager/css/uamLoginForm.css?ver=1.0",<br />
"https://www.syndikat.org/wp-content/plugins/user-access-manager/js/functions.js?ver=4.9.4",<br />
"https://www.syndikat.org/wp-content/plugins/wysija-newsletters/css/validationEngine.jquery.css?ver=2.8.1",<br />
"https://www.syndikat.org/wp-content/uploads/2017/11/s_miete_fr-200x116.png",<br />
"https://www.syndikat.org/wp-includes/js/jquery/jquery-migrate.min.js?ver=1.4.1",<br />
"https://www.syndikat.org/wp-includes/js/jquery/jquery.js?ver=1.12.4",<br />
"<a
href="https://www.syndikat.org/wp-includes/js/wp-emoji-release.min.js?ver=4.9.4"><em>https://www.syndikat.org/wp-includes/js/wp-emoji-release.min.js?ver=4.9.4</em></a>"</p>
<p> ],</p>
<p> "outlinks":{</p>
<p> "<a href="http://archive.org/"><em>https://archive.org/</em></a>":
"xxxxxx89b-f3ca-48d0-9ea6-1d1225e98695",</p>
<p> "<a href="https://other.com"><em>https://other.com</em></a>":
"yyyy89b-f3ca-48d0-9ea6-1d1225e98695"<br />
}}</p></td>
</tr>
</tbody>
</table>

Note that
*\"original_url\":\"*[*http://brewster.kahle.org/*](http://brewster.kahle.org/)*\"
*contains the final URL **after following potential redirects**.

Note that
*\"screenshot\":\"*[*http://web.archive.org/screenshot/http://brewster.kahle.org/*](http://web.archive.org/screenshot/http://brewster.kahle.org/)*\"
*is included in the response only when we use **capture_screenshot=1**.
In case there is a screenshot capture error, the result doesn't include
a \"screenshot\" field.

When **outlinks_availability=1** option is used, the outlinks would be
like the following:

<table>
<tbody>
<tr class="odd">
<td><p>"outlinks":{</p>
<p> "<a href="http://archive.org/"><em>https://archive.org/</em></a>":
{"timestamp": "20180102005040"},</p>
<p> "<a href="https://other.com"><em>https://other.com</em></a>":
{"timestamp": "20190102005040"},</p>
<p> "<a
href="https://other-not-captured.com"><em>https://other-not-captured.com</em></a>":
{"timestamp": null}<br />
}</p></td>
</tr>
</tbody>
</table>

In case the capture is pending, it may return:

<table>
<tbody>
<tr class="odd">
<td><p>{"status":"pending",</p>
<p> "job_id":"e70f33c7-9eca-4c88-826d-26930564d7c8",</p>
<p> "resources":[</p>
<p> "<a
href="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"><em>https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js</em></a>",</p>
<p> "<a
href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.21/jquery-ui.min.js"><em>https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.21/jquery-ui.min.js</em></a>",</p>
<p> "<a
href="https://cdn.onesignal.com/sdks/OneSignalSDK.js"><em>https://cdn.onesignal.com/sdks/OneSignalSDK.js</em></a>",</p>
<p> ]</p>
<p>}</p></td>
</tr>
</tbody>
</table>

In case there is an error, it may return:

<table>
<tbody>
<tr class="odd">
<td><p>{"status":"error",</p>
<p> "exception":"[Errno -2] Name or service not known",</p>
<p> "status_ext":"error:invalid-host-resolution",</p>
<p> "job_id":"2546c79b-ec70-4bec-b78b-1941c42a6374",</p>
<p> "message":"Couldn't resolve host for <a
href="http://example5123.com"><em>http://example5123.com</em></a>.",</p>
<p> "resources": []</p>
<p>}</p></td>
</tr>
</tbody>
</table>

[]{#anchor-5}Error codes

The error codes and messages may vary depending on the problem. Field
**status_ext** contains more information on the specific error type.

<table>
<tbody>
<tr class="odd">
<td><strong>status_ext</strong></td>
<td><strong>Description</strong></td>
</tr>
<tr class="even">
<td>error:bad-gateway</td>
<td>Bad Gateway for URL (HTTP status=502).</td>
</tr>
<tr class="odd">
<td>error:bad-request</td>
<td>The server could not understand the request due to invalid syntax.
(HTTP status=401)</td>
</tr>
<tr class="even">
<td>error:bandwidth-limit-exceeded</td>
<td>The target server has exceeded the bandwidth specified by the server
administrator. (HTTP status=509).</td>
</tr>
<tr class="odd">
<td>error:blocked</td>
<td>The target site is blocking us (HTTP status=999).</td>
</tr>
<tr class="even">
<td>error:blocked-client-ip</td>
<td><p>Anonymous clients which are listed in <a
href="https://www.spamhaus.org/xbl/"><em>https://www.spamhaus.org/xbl/</em></a>
or <a
href="https://www.spamhaus.org/sbl/"><em>https://www.spamhaus.org/sbl/</em></a>
lists (spams &amp; exploits) are blocked.</p>
<p>Tor exit nodes are excluded from this filter.</p></td>
</tr>
<tr class="odd">
<td>error:blocked-url</td>
<td>We use a URL block list based on Mozilla web tracker lists to avoid
unwanted captures.</td>
</tr>
<tr class="even">
<td>error:browsing-timeout</td>
<td>SPN2 back-end headless browser timeout.</td>
</tr>
<tr class="odd">
<td>error:capture-location-error</td>
<td>SPN2 back-end cannot find the created capture location. (system
error).</td>
</tr>
<tr class="even">
<td>error:cannot-fetch</td>
<td>Cannot fetch the target URL due to system overload.</td>
</tr>
<tr class="odd">
<td>error:celery</td>
<td>Cannot start capture task.</td>
</tr>
<tr class="even">
<td>error:filesize-limit</td>
<td>Cannot capture web resources over 2GB.</td>
</tr>
<tr class="odd">
<td>error:ftp-access-denied</td>
<td>Tried to capture an FTP resource but access was denied.</td>
</tr>
<tr class="even">
<td>error:gateway-timeout</td>
<td>The target server didn't respond in time. (HTTP status=504).</td>
</tr>
<tr class="odd">
<td>error:http-version-not-supported</td>
<td>The target server does not support the HTTP protocol version used in
the request for URL (HTTP status=505).</td>
</tr>
<tr class="even">
<td>error:internal-server-error</td>
<td>SPN internal server error.</td>
</tr>
<tr class="odd">
<td>error:invalid-url-syntax</td>
<td>Target URL syntax is not valid.</td>
</tr>
<tr class="even">
<td>error:invalid-server-response</td>
<td>The target server response was invalid. (e.g. invalid headers,
invalid content encoding, etc).</td>
</tr>
<tr class="odd">
<td>error:invalid-host-resolution</td>
<td>Couldn’t resolve the target host.</td>
</tr>
<tr class="even">
<td>error:job-failed</td>
<td>Capture failed due to system error.</td>
</tr>
<tr class="odd">
<td>error:method-not-allowed</td>
<td>The request method is known by the server but has been disabled and
cannot be used (HTTP status=405).</td>
</tr>
<tr class="even">
<td>error:not-implemented</td>
<td>The request method is not supported by the server and cannot be
handled (HTTP status=501).</td>
</tr>
<tr class="odd">
<td>error:no-browsers-available</td>
<td>SPN2 back-end headless browser cannot run.</td>
</tr>
<tr class="even">
<td>error:network-authentication-required</td>
<td>The client needs to authenticate to gain network access to the URL
(HTTP status=511).</td>
</tr>
<tr class="odd">
<td>error:no-access</td>
<td>Target URL could not be accessed (status=403).</td>
</tr>
<tr class="even">
<td>error:not-found</td>
<td>Target URL not found (status=404).</td>
</tr>
<tr class="odd">
<td>error:not-implemented</td>
<td>The request method is not supported by the server and cannot be
handled for URL (HTTP status=501).</td>
</tr>
<tr class="even">
<td>error:proxy-error</td>
<td>SPN2 back-end proxy error.</td>
</tr>
<tr class="odd">
<td>error:protocol-error</td>
<td>HTTP connection broken. (A possible cause of this error is
"IncompleteRead").</td>
</tr>
<tr class="even">
<td>error:read-timeout</td>
<td>HTTP connection read timeout.</td>
</tr>
<tr class="odd">
<td>error:soft-time-limit-exceeded</td>
<td>Capture duration exceeded 45s time limit and was terminated.</td>
</tr>
<tr class="even">
<td>error:service-unavailable</td>
<td>Service unavailable for URL (HTTP status=503).</td>
</tr>
<tr class="odd">
<td>error:too-many-daily-captures</td>
<td>This URL has been captured 10 times today. We cannot make any more
captures.</td>
</tr>
<tr class="even">
<td>error:too-many-redirects</td>
<td>Too many redirects. SPN2 tries to follow 3 redirects
automatically.</td>
</tr>
<tr class="odd">
<td>error:too-many-requests</td>
<td><p>The target host has received too many requests from SPN and it is
blocking it. (HTTP status=429).</p>
<p>Note that captures to the same host will be delayed for 10-20s after
receiving this response to remedy the situation.</p></td>
</tr>
<tr class="even">
<td>error:user-session-limit</td>
<td>User has reached the limit of concurrent active capture
sessions.</td>
</tr>
<tr class="odd">
<td>error:unauthorized</td>
<td>The server requires authentication (HTTP status=401).</td>
</tr>
<tr class="even">
<td>error:max-daily-bandwidth</td>
<td>An authenticated user can archive up to 5GB per day.</td>
</tr>
<tr class="odd">
<td>error:max-daily-bandwidth-from-ip</td>
<td>An anonymous user can archive up to 2GB per day.</td>
</tr>
<tr class="even">
<td>error:max-daily-bandwidth-host</td>
<td>SPN2 can archive up to 100GB per day from a host.</td>
</tr>
</tbody>
</table>

In case you used option \`capture_outlinks=1\`, the result outlinks
include the job_id for each outlink so that you could check its status
later. Else, outlinks key contains the list of URLs only.

You can access the created capture using the following URL pattern:

|                                                            |
|------------------------------------------------------------|
| https://web.archive.org/web/\<timestamp\>/\<original_url\> |

**Advanced status request usage**

To see the status of **multiple captures**, use parameter **job_ids**
and a comma separated list of values:

|                                                                                                                                                                                                                                                                                                                           |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| curl -X POST -H \"Accept: application/json\" -d\'job_ids=ac58789b-f3ca-48d0-9ea6-1d1225e98695,ac58789b-f3ca-48d0-9ea6-xxxxxx, ac58789b-f3ca-48d0-9ea6-yyyyyyyyy\' \--cookie \"logged-in-sig=AAAAAAAAAA;logged-in-user=user1%40archive.org;\" [*https://web.archive.org/save/status*](https://web.archive.org/save/status) |

To see the capture status of all outlinks, use parameter
**job_id_outlinks** and the job_id of the parent capture:

|                                                                                                                                                                                                                                                                 |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| curl -X POST -H \"Accept: application/json\" -d\'job_id_outlinks=ac58789b-f3ca-48d0-9ea6-1d1225e98695\' \--cookie \"logged-in-sig=AAAAAAAAAA;logged-in-user=user1%40archive.org;\" [*https://web.archive.org/save/status*](https://web.archive.org/save/status) |

[]{#anchor-6}User status

You can see the current number of active and available session of your
user account using the following:

|                                                                                                                                    |
|------------------------------------------------------------------------------------------------------------------------------------|
| curl -X GET -H \"Accept: application/json\" -H \"Authorization: LOW myaccesskey:mysecret\" http://web.archive.org/save/status/user |

To avoid getting a stale cache response, it is better to use a URL like
this:
[*http://web.archive.org/save/status/user?\_t=1602606392499*](http://web.archive.org/save/status/user?_t=1602606392499)
where \_t is a random variable.

The response will be like:

|                                     |
|-------------------------------------|
| {\"available\":12,\"processing\":3} |

[]{#anchor-7}System status

You can check if the service is overloaded using the following:

|                                                                                       |
|---------------------------------------------------------------------------------------|
| curl -X GET -H \"Accept: application/json\" http://web.archive.org/save/status/system |

If everything is fine, it may return:

|                     |
|---------------------|
| {\"status\":\"ok\"} |

If the service is overloaded, it may return:

|                                                                                                  |
|--------------------------------------------------------------------------------------------------|
| {\"status\":\"Save Page Now servers are temporarily overloaded. Your captures may be delayed.\"} |

To be clear, SPN will still work fine in this case, besides some delays.

If there is a critical problem, there will be an HTTP status=502
response.

[]{#anchor-8}Tips for faster captures

The following options have a real impact on the speed of your captures.

- If you don't need to know if your capture is the first in the Archive,
  > please use **skip_first_archive=1.**

- If you are sure that the target URL is not an HTML page and can be
  > downloaded via a plain HTTP request, use option **force_get=1.**

- If the target HTML page is plain and you don't need to run any JS
  > behavior to download all content (JS behaviors scroll down the page
  > automatically and/or trigger AJAX requests), use
  > **js_behavior_timeout=0.**

- Do NOT use **capture_outlinks=1 **unless it is really necessary to
  > capture all outlinks. If you are interested in capturing a specific
  > outlink, make a capture, check the list of outlinks returned by SPN2
  > and capture only the specific outlink(s) you need.

[]{#anchor-9}Limitations

The operation of SPN2 is limited in several ways as described in the
following table. The aim of these limitations is to ensure the
performance and stability of the application.

<table>
<tbody>
<tr class="odd">
<td><strong>Limitation</strong></td>
<td><strong>Description</strong></td>
</tr>
<tr class="even">
<td>Network connection timeout = 10s</td>
<td>If we try connecting to a target URL and it takes more than 10s to
respond, we consider the server unresponsive and return a capture
error.</td>
</tr>
<tr class="odd">
<td>Max captures per minute for authenticated users = 12 and for
anonymous users = 4.</td>
<td>Any user can do N captures per minute. If you try to start more,
SPN2 returns an error.</td>
</tr>
<tr class="even">
<td>Max web page capture time = 50s</td>
<td>SPN2 browsers can spend up to 50s visiting a target URL and running
JS behaviors. If web page capture hasn’t finished after that time, we
terminate the browser and check if we have downloaded sufficient content
to consider this a successful capture.</td>
</tr>
<tr class="odd">
<td>Max capture duration = 2m</td>
<td>The total time spent capturing any URL cannot be over 2m.</td>
</tr>
<tr class="even">
<td>Max JS behavior runtime = 7s (configurable)</td>
<td>The total time running JS events (scroll down, mouse over, etc)
cannot be over 5s by default. This is configurable using param:
<em>js_behavior_timeout=&lt;N&gt;</em></td>
</tr>
<tr class="odd">
<td>Max redirects = 3</td>
<td>SPN2 tries to follow redirects automatically.</td>
</tr>
<tr class="even">
<td>Max resource size = 2GB</td>
<td>The max file size SPN2 can download.</td>
</tr>
<tr class="odd">
<td>Max number of outlinks captured using capture_outlinks option =
100</td>
<td><p>SPN2 captures the first N outlinks automatically when using
option capture_outlinks.</p>
<p>Outlinks are ordered using some rules before selecting the first
N:</p>
<ol type="1">
<li><blockquote>
<p>PDF</p>
</blockquote></li>
<li><blockquote>
<p>Epub</p>
</blockquote></li>
<li><blockquote>
<p>URLs containing substrings "new" or "update"</p>
</blockquote></li>
<li><blockquote>
<p>URLs of the same domain as the original capture URL.</p>
</blockquote></li>
</ol>
<p>Please note that if you don’t use option capture_outlinks, you get a
list of all outlinks without any filtering or ranking. You could use
that list to download any URLs necessary.</p></td>
</tr>
<tr class="even">
<td>Max number of outlinks returned = 1000</td>
<td>SPN2 just returns a list of outlinks if "capture outlinks" is not
selected. This list is limited to 1000 items.</td>
</tr>
<tr class="odd">
<td>Max number of embeds returned = 1000</td>
<td>SPN2 tracks all captured embeds and lists them in "resources". This
list is limited to 1000 items.</td>
</tr>
<tr class="even">
<td>Max number of links captured from emails in <a
href="mailto:spn@archive.org"><em>spn@archive.org</em></a> = 500</td>
<td>SPN2 tries to capture the first 500 links in emails sent to <a
href="mailto:spn@archive.org"><em>spn@archive.org</em></a>. </td>
</tr>
<tr class="odd">
<td>Max captures per day for anonymous users = 4k</td>
<td>Anonymous users can use SPN2 but their total captures per day cannot
be more than this limit.</td>
</tr>
<tr class="even">
<td>Max captures per day for authenticated users = 100k</td>
<td>The captures of authenticated users cannot be more than this limit
per day. If you need to make more captures, please contact <a
href="mailto:info@archive.org"><em>info@archive.org</em></a>. </td>
</tr>
<tr class="odd">
<td>Max captures per day for a URL = 10</td>
<td>It is possible to capture the same URL only 10 times per day.</td>
</tr>
<tr class="even">
<td>Blocked URLs</td>
<td>SPN2 uses Mozilla web tracker block lists to avoid capturing some
URLs. You may get an "error:blocked-url" when trying to make a
capture.</td>
</tr>
<tr class="odd">
<td>Artificial delays for multiple concurrent captures on the same
host.</td>
<td><p>When we run more than 20 concurrent captures on the same host, we
introduce an artificial delay on subsequent captures to avoid
overloading the target and blocking SPN2.</p>
<p>The delay algorithm is:</p>
<p>When concurrent_capture_number &gt; 20 for the same host, delay
concurrent_capture_number/5 sec.</p>
<p>For example: if concurrent_capture_number = 50, delay a new capture
by 50/5 = 10 sec.</p></td>
</tr>
<tr class="even">
<td>Max emails processed by <a
href="mailto:spn@archive.org"><em>spn@archive.org</em></a> service per
user per day= 10</td>
<td>You can send HTML emails with links to capture at <a
href="mailto:spn@archive.org"><em>spn@archive.org</em></a>. The system
processes 10 emails per user per day and discards the rest.</td>
</tr>
<tr class="odd">
<td>Max screenshot size is 4MB</td>
<td>If you select "Save screen shot" and its size is &gt; 4MB, it is
skipped to avoid system overload.</td>
</tr>
<tr class="even">
<td>Max captures’ size per day is 2GB for anonymous users.</td>
<td>Anonymous users can capture no more than 2GB total per day.</td>
</tr>
<tr class="odd">
<td>Max captures’ size per day is 5GB for authenticated users.</td>
<td>Authenticated users can capture no more than 5GB total per day.</td>
</tr>
</tbody>
</table>

[]{#anchor-10}Example PHP script using the SPN2 API to capture a URL

<table>
<tbody>
<tr class="odd">
<td><p>&lt;?php</p>
<p>/**</p>
<p> * Example PHP script which captures a URL via the SPN2 API.</p>
<p> * Note that this script doesn't include proper exception handling
and is not</p>
<p> * optimised for production use.</p>
<p> * Tested with PHP 7.0 and the PHP curl extension on Ubuntu
16.04.</p>
<p> *</p>
<p> * Full SPN2 API reference:</p>
<p> *
https://docs.google.com/document/d/1Nsv52MvSjbLb2PCpHlat0gkzw0EvtSgpKHu4mk0MnrA/edit</p>
<p> *</p>
<p> * Archive.org credentials are required to use the SPN2 API,</p>
<p> * get your credentials from https://archive.org/account/s3.php</p>
<p> */</p>
<p>$KEY = "XXX";</p>
<p>$SECRET = "YYY";</p>
<p>$TARGET_URL = "https://bbc.co.uk";</p>
<p>$headers = array("Accept: application/json",</p>
<p> "Content-Type: application/x-www-form-urlencoded;charset=UTF-8",</p>
<p> "Authorization: LOW {$KEY}:{$SECRET}");</p>
<p>$params = array('url'=&gt;$TARGET_URL);</p>
<p>$ch = curl_init();</p>
<p>curl_setopt($ch, CURLOPT_URL, "https://web.archive.org/save");</p>
<p>curl_setopt($ch, CURLOPT_POST, 1);</p>
<p>curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));</p>
<p>curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);</p>
<p>curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);</p>
<p>$response = curl_exec($ch);</p>
<p>curl_close($ch);</p>
<p>$data = json_decode($response, true);</p>
<p>$job_id = $data['job_id'];</p>
<p>print("Capture started, job id: {$job_id}\n");</p>
<p>while(true) {</p>
<p> sleep(5);</p>
<p> $response =
file_get_contents("http://web.archive.org/save/status/{$job_id}");</p>
<p> $data = json_decode($response, true);</p>
<p> if ($data['status'] == 'success') {</p>
<p> print("Capture complete:
https://web.archive.org/web/{$data['timestamp']}/{$data['original_url']}\n");</p>
<p> break;</p>
<p> } else if ($data['status'] == 'error') {</p>
<p> print("Error: {$data['message']}\n");</p>
<p> break;</p>
<p> }</p>
<p> print("Wait, still capturing...\n");</p>
<p>}</p></td>
</tr>
</tbody>
</table>

[]{#anchor-11}Frequently Asked Questions

**Q1. I can see the page
**[***http://example.com/***](http://example.com/)** from my web browser
but when I try to capture it, I get an error: \"Live page is not
available\".**

Before SPN2 captures a URL, it tries to do a quick HTTP HEAD and if that
fails an HTTP GET to see if the target URL is online. If these requests
fail, we return an error: *\"Live page is not available\"*. If they are
successful, we make the capture using our headless browser. Also, we
cache the result for 10 min to speedup this check for subsequent
requests. This check may return an invalid result for many reasons:

1.  The site may have blocked requests from IA IPs in general.

2.  We are doing many captures on the same site at the same time (e.g.
    > by other SPN2 users or via \"capture outlinks\"), the target site
    > receives too many connections from SPN2 and its firewall/web
    > server blocks them. In these cases, the capture result would be
    > \"Live page is not available\" but the site would be perfectly
    > fine for you as you are using it from your home IP address. To
    > mitigate this issue, we are delaying captures from the same host
    > when there are 50+ concurrent captures.

3.  Sites may actually be down for a few seconds or more due to
    > technical issues on their end (e.g. network outages, server
    > problems, etc).

**Q2. I'm trying to capture a web page that contains a lot of links
using the \"capture outlinks\" option but no outlinks are captured.**

SPN2 can extract outlinks from many file types: HTML pages, PDF, RSS,
XML and JSON files. For each file type, it runs a special link extractor
software for 30 sec. For HTML pages, it's a JS script that extracts URLs
from a\[href\], area\[href\], a\[onclick\], a\[ondblclick\]:
[*https://github.com/internetarchive/brozzler/blob/master/brozzler/js-templates/extract-outlinks.js*](https://github.com/internetarchive/brozzler/blob/master/brozzler/js-templates/extract-outlinks.js)

If SPN2 cannot extract outlinks from a URL, one of the following issues
may occur:

1.  The outlink extraction couldn't finish processing in 30 sec and was
    > terminated.

2.  The total URL capture took too long (the limit is 90 sec) and there
    > wasn't time to run the outlink extraction in time.

3.  The target URL doesn't have links or they are encoded in a way that
    > is not supported by the outlink extraction software (e.g. using
    > some obscure HTML element attributes and events or an encrypted
    > PDF).

**Q3. When I try to do a capture, I get a message saying***** \"Your
capture will begin in XXs.\". *****Is SPN2 overloaded?**

When we run more than 20 concurrent captures on the same host, we
introduce an artificial delay on subsequent captures to avoid
overloading the target and blocking SPN2. The delay algorithm is:

When concurrent_capture_number \> 20 for the same host, delay
concurrent_capture_number/5 sec.

For example: if concurrent_capture_number = 50, delay a new capture by
50/5 = 10 sec.

By \"concurrent captures\", we mean captures performed in the last 60
sec.

In addition to that, if a target site returns HTTP status=429 (too many
requests), we delay any subsequent captures for 10 to 20 sec. This rule
applies for 60 sec after receiving the status=429 response.
