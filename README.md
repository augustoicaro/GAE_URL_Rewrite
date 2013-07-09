#GAE URL Rewrite

This is a clone for [Paulo Jerônimo's project](https://code.google.com/p/dropbprox/) and [shin1katayama's project](https://code.google.com/r/shin1katayama-dropbprox-directoryindex/) with some improvements.

#Summary

A GAE proxy to your Dropbox account including main page redirect and Directory Index.

##Description

The GAE URL Rewrite Modified aims to allow you to use your own domain to get files published in your host site. So, after setting up your host site account number at the application and publish it on Google App Engine (GAE), you will access your files in the host site linking them to a more significant domain than that presented by URL http://dl.dropbox.com/u/YOURDROPBOXNUMBER for example.

This code is a very simple reduction/adaptation of [mirrorrr project](http://code.google.com/p/mirrorrr/) {by [Brett Slatkin](http://www.onebigfluke.com/)} held specifically to achieve the goals to build a proxy for public files from a user account in the Dropbox. If you want a full (and FREE) proxy to run on GAE, use the mirrorrr!

##Motivation

I was looking for alternative to host my html pages in dropbox and others host site masking with my domain. With just a few searches on Google, I found a [Paulo Jerônimo's project](https://code.google.com/p/dropbprox/) and clone for this project, [shin1katayama's project](https://code.google.com/r/shin1katayama-dropbprox-directoryindex/). Thus, I adapted their code to suit my needs.

##Debug

Debug is simple, go in GAE administrator menu, in left tab click in LOGs.
Done! Now you can see all debug text.

##Installation

* Create a new project on GAE.
  * For example, I created a project named pj74arqs. A good tutorial about how to do this (for windows users) is the post "[Setup your own Proxy Server in 5 Minutes for Free](http://www.labnol.org/internet/setup-proxy-server/12890/)"
* Change application variable at file app.yaml to the name of your created project on GAE;
* Change DROPBOX_NUMBER variable at file mirror.py to your own Dropbox number;
* Publish the application on GAE;
  * Windows users: see this [post](http://www.labnol.org/internet/setup-proxy-server/12890/);
* Optional: Change the domain of the published application.
  * In my case, after publish the application, the domain was pj74arqs.appspot.com. But, this wasn't good for me yet. So, I changed the URL for that application to my subdomain: a.paulojeronimo.com. That was much better!

##Use

* Instead of access your files using the Dropbox URL (http://dl.dropbox.com/u/YOURDROPBOXNUMBER) you can now use the GAE application URL.
  * In my case, instead of access files at http://dl.dropbox.com/u/345266, I can now do that using http://a.paulojeronimo.info. For example, the files http://dl.dropbox.com/u/345266/curriculo/curriculo-pj.html and http://a.paulojeronimo.info/curriculo/curriculo-pj.html (Paulo's portuguese resume ;-) are the same, but the second is much more expressive, isn't it?
  * Or use to view yours html page in your folder. For example, if you put http://a.paulojeronimo.info/, the page is redirect to http://a.paulojeronimo.info/index.html. And this happens to Folder in list of folders, http://a.paulojeronimo.info/test, redirect to http://a.paulojeronimo.info/test/index.php
* Update a file in your Dropbox account and refresh your URL. You will see that was updated in your proxy too!
