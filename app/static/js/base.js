/*
 * @Author: your name
 * @Date: 2020-12-30 15:48:08
 * @LastEditTime: 2021-01-12 04:04:05
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \2011cw2\app\static\js\base.js
 */

$(window).ready(function(){
    $("#loginBox").hide();
    $(".addc").hide();
    var loginBox=document.getElementById("loginBox");//获取窗体
    var top=($(window).height() - $("#loginBox").height())/2 + "px";
    var left=($(window).width() - $("#loginBox").width())/2 + "px";
    loginBox.style.top=top;
    loginBox.style.left=left;
     $(".close").click(function() {
         $("#loginBox").hide();
     }); 
});

$(window).resize(function(){

    var loginBox=document.getElementById("loginBox");//获取窗体
    var top=($(window).height() - $("#loginBox").height())/2 + "px";
    var left=($(window).width() - $("#loginBox").width())/2 + "px";
    if(left+350>$(window).width()){left=0;}
    loginBox.style.top=top;
    loginBox.style.left=left;
});

$(".loginbutton").click(function(){

    $("#loginBox").show();

});

$("#logout").click(function(){

    session.clear();
    refresh();
});

$(".unloginc").click(function(){

    alert("Please log in!!")
    $("#loginBox").show()
});

$(function(){

    $("#acat").val($("#asel").val())
    $("#asel").change(function(){
        $("#acat").val($("#asel").val())
    });
});

$(".addcat").click(function(){

    $(".addc").show()
});
