var console_style = 'color: tomato; -webkit-text-stroke: 4px purple; font-size:30px;';
console.log('%cHi!', console_style );

function today()
{
    let d = new Date()
    let year = d.getFullYear()
    let month = d.getMonth() + 1
    let day = d.getDate()
    if (month <= 9)
    {
        month = "0" + month
    }
    if (day <= 9)
    {
        day = "0" + day
    }
    let today = year + "-" + month + "-" + day
    return today
}

function LoadText(Text, Div)
{
    let abouttxt = Text
    let abouttxt_parts = abouttxt.innerHTML.split("\n")
    console.log(abouttxt_parts)
    let AboutDiv = Div
    for(let i = 0; i <= abouttxt_parts.length - 1; i++)
    {
        console.log(i + " " + abouttxt_parts[i])
        if (i == 0)
        {
            let topaboutelem = document.createElement("p")
            let text = document.createTextNode(abouttxt_parts[i])
            topaboutelem.appendChild(text)
            topaboutelem.classList.add("about")
            topaboutelem.classList.add("abouttop")
            AboutDiv.appendChild(topaboutelem)
            let newline = document.createElement("br")
            AboutDiv.appendChild(newline)
            continue
        }
        if (i == abouttxt_parts.length)
        {
            let bottomaboutelem = document.createElement("p")
            let text = document.createTextNode(abouttxt_parts[i - 1])
            bottomaboutelem.classList.add("about")
            bottomaboutelem.classList.add("aboutbottom")
            bottomaboutelem.appendChild(text)
            AboutDiv.appendChild(bottomaboutelem)
            let newline = document.createElement("br")
            AboutDiv.appendChild(newline)
            continue
        }
        let aboutelem = document.createElement("p")
        let text = document.createTextNode(abouttxt_parts[i])
        aboutelem.appendChild(text)
        aboutelem.classList.add("about")
        AboutDiv.appendChild(aboutelem)
        newline = document.createElement("br")
        AboutDiv.appendChild(newline)
    }
    abouttxt.remove()
}

window.onscroll = function () 
{
    scrollFunction();
}

function scrollFunction() 
{
    try
    {
        let scrollMax=$(document).height()-$(window).height();
        if (Math.min(document.body.scrollTop, scrollMax) > 70 || Math.min(document.documentElement.scrollTop, scrollMax) > 70 && document.documentElement.scrollTop<=scrollMax)
        {
            document.querySelector('#navimage').classList.add('downScroll')
        }
        else if (document.body.scrollTop < 5 && document.documentElement.scrollTop < 5)
        {
            document.querySelector('#navimage').classList.remove('downScroll')
        }
    }
    catch (ReferenceError)
    {}
}

function SKaRVroom()
{
    elem = document.getElementById("SKaRtoiletvroom")
    elem.style.bottom = "100em"
}

var id = null;
function VroomAnimation()
{
    let elem = document.getElementById("vroom")
    let pos = 33
    let x = 0
    if (pos !== 33)
    {
        return
    }
    clearInterval(id)
    id = setInterval(frame, 1)
    function frame() 
    {
        if (pos == 30)
        {
            clearInterval(id)
        }
        else if (pos >= screen.width) 
        {    
            pos = -30
            try
            {
                clearInterval(id2)
            }
            catch (ReferenceError)
            {
                return
            }
            id2 = setInterval(frame2, 1)
            function frame2()
            {
                if (pos < 30)
                {
                    pos += 0.5
                    elem.style.left = pos + 'px'
                }
                else
                {
                    clearInterval(id2)
                    return
                }
            }
            return
        } 
        else 
        {
            pos += 3
        }
        elem.style.left = pos + 'px'
    }
}

function selectall1()
{
    let elem = document.getElementById("all1")
    if (elem.checked)
    {
        for (i in document.getElementsByClassName("itemallinput1"))
        {
            document.getElementsByClassName("itemallinput1")[i].checked = true
        }
    }
    else    
    {
        for (i in document.getElementsByClassName("itemallinput1"))
        {
            document.getElementsByClassName("itemallinput1")[i].checked = false
        }
    }
}

function selectall2()
{
    let elem = document.getElementById("all2")
    if (elem.checked)
    {
        for (i in document.getElementsByClassName("itemallinput2"))
        {
            document.getElementsByClassName("itemallinput2")[i].checked = true
        }
    }
    else    
    {
        for (i in document.getElementsByClassName("itemallinput1"))
        {
            document.getElementsByClassName("itemallinput2")[i].checked = false
        }
    }
}

function selectall3()
{
    let elem = document.getElementById("all3")
    if (elem.checked)
    {
        for (i in document.getElementsByClassName("itemallinput3"))
        {
            document.getElementsByClassName("itemallinput3")[i].checked = true
        }
    }
    else    
    {
        for (i in document.getElementsByClassName("itemallinput3"))
        {
            document.getElementsByClassName("itemallinput3")[i].checked = false
        }
    }
}

function allEqual(list, count)
{
    var i 
    let res = true
    for (i = 0; i <= count; i++)
    {
        if (list[i].checked !== list[0].checked)
        {
            res = false
            break
        }
    }
    return res

}

function checkselectall1()
{
    elems = document.getElementsByClassName("itemallinput1")
    selectall = document.getElementById("all1")
    if (allEqual(elems, 6))
    {
        if (elems[0].checked == true)
        {
            selectall.checked = true
        }
        else if (elems[0].checked == false)
        {
            selectall.checked = false
        }
    }
    else if (allEqual(elems, 6) == false)
    {
        selectall.checked = false
    }
}

function checkselectall2()
{
    elems = document.getElementsByClassName("itemallinput2")
    selectall = document.getElementById("all2")
    if (allEqual(elems, 2))
    {
        if (elems[0].checked == true)
        {
            selectall.checked = true
        }
        else if (elems[0].checked == false)
        {
            selectall.checked = false
        }
    }
    else if (allEqual(elems, 2) == false)
    {
        selectall.checked = false
    }
}

function checkselectall3()
{
    elems = document.getElementsByClassName("itemallinput3")
    selectall = document.getElementById("all3")
    if (allEqual(elems, 2))
    {
        if (elems[0].checked == true)
        {
            selectall.checked = true
        }
        else if (elems[0].checked == false)
        {
            selectall.checked = false
        }
    }
    else if (allEqual(elems, 2) == false)
    {
        selectall.checked = false
    }
}

function orderonlyone(elem)
{
    let OrderList = document.getElementsByClassName("OrderElem")
    let ElemId = elem.id

    if (elem.checked == false)
    {
        for (i in OrderList)
        {
            if (OrderList[i].checked == true)
            {
                break
            }
        }
        elem.checked = true
    }
    else if (elem.checked == true)
    {
        for (i in OrderList)
        {
            if (OrderList[i].checked == true)
            {
                OrderList[i].checked = false
            }
        }
        elem.checked = true
    }
}


function dropdown1(elem)
{
    if (elem.checked) 
    {
        let touch = document.getElementsByClassName("touch")
        for (i in touch)
        {
            touch[i].checked = false
        }
        elem.checked = true
        let tostyle = document.querySelector("#touch1:checked + .slide")
        tostyle.style.height = "7em"
        document.getElementById("slide2").style.height = "0px"
        document.getElementById("slide3").style.height = "0px"
        document.getElementById("slide4").style.height = "0px"
        document.getElementById("slide5").style.height = "0px"
        document.getElementById("slide6").style.height = "0px"
    }
    else if (elem.checked == false)
    {
        let tostyle = document.querySelector("#touch1 + .slide")
        tostyle.style.height = "0px"
    }
}

function dropdown2(elem)
{
    if (elem.checked) 
    {
        let touch = document.getElementsByClassName("touch")
        for (i in touch)
        {
            touch[i].checked = false
        }
        elem.checked = true
        let tostyle = document.querySelector("#touch2:checked + .slide")
        tostyle.style.height = "12.6em"
        document.getElementById("slide1").style.height = "0px"
        document.getElementById("slide3").style.height = "0px"
        document.getElementById("slide4").style.height = "0px"
        document.getElementById("slide5").style.height = "0px"
        document.getElementById("slide6").style.height = "0px"
    }
    else if (elem.checked == false)
    {
        let tostyle = document.querySelector("#touch2 + .slide")
        tostyle.style.height = "0em"
    }
}

function dropdown3(elem)
{
    if (elem.checked) 
    {
        let touch = document.getElementsByClassName("touch")
        for (i in touch)
        {
            touch[i].checked = false
        }
        elem.checked = true
        let tostyle = document.querySelector("#touch3:checked + .slide")
        tostyle.style.height = "5em"
        document.getElementById("slide1").style.height = "0px"
        document.getElementById("slide2").style.height = "0px"
        document.getElementById("slide4").style.height = "0px"
        document.getElementById("slide5").style.height = "0px"
        document.getElementById("slide6").style.height = "0px"
    }
    else if (elem.checked == false)
    {
        let tostyle = document.querySelector("#touch3 + .slide")
        tostyle.style.height = "0em"
    }
}

function dropdown4(elem)
{
    if (elem.checked) 
    {
        let touch = document.getElementsByClassName("touch")
        for (i in touch)
        {
            touch[i].checked = false
        }
        elem.checked = true
        let tostyle = document.querySelector("#touch4:checked + .slide")
        tostyle.style.height = "8em"
        document.getElementById("slide1").style.height = "0px"
        document.getElementById("slide2").style.height = "0px"
        document.getElementById("slide3").style.height = "0px"
        document.getElementById("slide5").style.height = "0px"
        document.getElementById("slide6").style.height = "0px"
    }
    else if (elem.checked == false)
    {
        let tostyle = document.querySelector("#touch4 + .slide")
        tostyle.style.height = "0em"
    }
}

function dropdown5(elem)
{
    if (elem.checked) 
    {
        let touch = document.getElementsByClassName("touch")
        for (i in touch)
        {
            touch[i].checked = false
        }
        elem.checked = true
        let tostyle = document.querySelector("#touch5:checked + .slide")
        tostyle.style.height = "7em"
        document.getElementById("slide1").style.height = "0px"
        document.getElementById("slide2").style.height = "0px"
        document.getElementById("slide3").style.height = "0px"
        document.getElementById("slide4").style.height = "0px"
        document.getElementById("slide6").style.height = "0px"
    }
    else if (elem.checked == false)
    {
        let tostyle = document.querySelector("#touch5 + .slide")
        tostyle.style.height = "0em"
    }
}

function dropdown6(elem)
{
    if (elem.checked) 
    {
        let touch = document.getElementsByClassName("touch")
        for (i in touch)
        {
            touch[i].checked = false
        }
        elem.checked = true
        let tostyle = document.querySelector("#touch6:checked + .slide")
        tostyle.style.height = "7em"
        document.getElementById("slide1").style.height = "0px"
        document.getElementById("slide2").style.height = "0px"
        document.getElementById("slide3").style.height = "0px"
        document.getElementById("slide4").style.height = "0px"
        document.getElementById("slide5").style.height = "0px"
    }
    else if (elem.checked == false)
    {
        let tostyle = document.querySelector("#touch6 + .slide")
        tostyle.style.height = "0em"
    }
}

function FilterBar()
{
    let arrow = document.getElementById("arrow")
    let FilterBar = document.getElementById("FilterBar")
    if (FilterBar.style.left == "0px")
    {
        FilterBar.style.left = "-100%"
        arrow.style.marginLeft = "0"
        arrow.style.transform = "rotate(0deg)"
        arrow.style.marginLeft = ".5em"

    }
    else
    {
        FilterBar.style.left = "0"
        arrow.style.marginLeft = "13em"
        arrow.style.transform = "rotate(180deg)"
    }
}