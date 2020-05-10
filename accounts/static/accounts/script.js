//append_attribute function
let append_attrib=function(variable,value)
{
    //storing main variables 
    let url=window.location.href
    let universe_regex=new RegExp('[\\w]+=[\\w"%-]+','g')
    let variable_list=url.match(universe_regex)
    let variable_count=0
    if (variable_list !=null)
        variable_count=variable_list.length
    let check=url.includes(variable)
    //main logic
    if(check==true) // if the varialbe is already existed
    {
        regex=new RegExp(variable+'=[\\w%"-]+','g')
        newValue=`${variable}=${value}`
        oldValue=url.match(regex)[0]
        num_extract_regex=new RegExp('\\d+','g')
        old_value_num=Number(oldValue.match(num_extract_regex)[0])
        if(variable=='filter' && old_value_num==value) // particular for filter
        {   
            if (variable_count==1)
                window.location.href=url.replace('?'+oldValue,'')
            else
            {
                index=variable_list.indexOf(oldValue)
                if (index==0)
                window.location.href=url.replace('?'+oldValue+'&','?')
                else
                window.location.href=url.replace('&'+oldValue,'')
            }
            return 
        }
        window.location.href=url.replace(regex,newValue)
    }
    else // creating new variable 
    {
        newValue=`${variable}=${value}`
        if(variable_count!=0)
            window.location.href=url+'&'+newValue
        else
            window.location.href=url+'?'+newValue
    }
}
// append to json
function append_to_json(variable,value)
{
    //storing main variables
    let url=window.location.href
    let universe_regex=new RegExp('[\\w]+=[\\w"%-]+','g')
    let variable_list=url.match(universe_regex)
    let variable_count=0
    if (variable_list !=null)
        variable_count=variable_list.length
    let check=url.includes(variable)
    //main logic
    if(check==true) // if the variable is already existed
    {
        regex=new RegExp(variable+'=[\\w%"-]+','g')
        json_string_with_variable=url.match(regex)[0]
        json_string=json_string_with_variable.replace(`${variable}=`,'')
        obj=uriToJSON(json_string)
        if (obj.tags.includes(value))
        {
            index=obj.tags.indexOf(value)
            obj.tags.splice(index,1)
        }
        else
            obj.tags.push(value)
        newValue=`${variable}=${jsonToURI(obj)}`
        if (obj.tags.length==0)
        {
            if(variable_count==1)
                window.location.href=url.replace('?'+json_string_with_variable,'')
            else
            {
                index=variable_list.indexOf(json_string_with_variable)
                if (index==0)
                    window.location.href=url.replace('?'+json_string_with_variable+'&','?')
                else
                    window.location.href=url.replace('&'+json_string_with_variable,'')
            }
            return 
        }
        window.location.href=url.replace(regex,newValue)
        return
    }
    else
    {
        obj={
            tags:[value,],
        }
        newValue=`${variable}=${jsonToURI(obj)}`
        if (variable_count!=0)
            window.location.href=url+'&'+newValue
        else
            window.location.href=url+'?'+newValue
    }
}
//handling tags
django_list=document.querySelectorAll('#django')
    django_list.forEach((django)=>
    {
        django.addEventListener('click',()=>
        {
            if (django.classList.contains('tag-clicked'))
            {
                django.classList.remove('tag-clicked')
            }
            else
            {
                django.classList.add('tag-clicked')
            }
        })
    })
//converting func from uri to Json object
function uriToJSON(urijson)
    { 
    return JSON.parse(decodeURIComponent(urijson));
    }
//converting func from json to uri format
function jsonToURI(json)
{ 
    return encodeURIComponent(JSON.stringify(json));
}
