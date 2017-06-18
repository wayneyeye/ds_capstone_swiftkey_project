#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)


# Define UI for application that draws a histogram
ui <- fluidPage(
  textInput("caption", "Input Text", "What a wonderful"),
  verbatimTextOutput("value")
)
server <- function(input, output) {
  library(jsonlite)
  nGramDict<-read_json('data/mixed-nGramDict_skim_10.json')
  
  trim <- function (x) gsub("^\\s+|\\s+$", "", x)
  trimPunctuations <- function (x) gsub("^[[:punct:]]+|[[:punct:]]+$", "", x)
  
  cleanInputPredict <- function(test_input){
    cleanedInput<-list()
    test_input_t<-test_input
    test_input_t<-trim(test_input_t)
    test_input_t<-tolower(test_input_t)
    test_input_t<-strsplit(test_input_t,split='\\s+')
    for (item in test_input_t){
      item<-trimPunctuations(item)
      item<-gsub("^.*\\d+.*$", "<quantity>", item)
      cleanedInput<-append(cleanedInput,item)
    }
    return(cleanedInput)
  }

  predictCore<-function(input_tokens,out_len=5){
    input_tokens_o<-input_tokens
    if (length(input_tokens)<1){
      output_list<<-append(output_list,nGramDict[['_r']])
    }
    else{
      input_idtokens<-list()
      for (w in input_tokens){
        w<-trim(w)
        #print(w)
        if (w %in% names(nGramDict$`_word2id`$`_word`)){
          WID<-toString(nGramDict$`_word2id`$`_word`[w])
          #print(nextWID)
          input_idtokens<-append(input_idtokens,WID)
          #print(input_idtokens)
        }
        else{
          input_idtokens<-append(input_idtokens,'NA')
        }
      }
      #print(input_idtokens)
      input_tokens<-input_idtokens
      nGram_flag<-TRUE
      i<-1
      p_Dict<-nGramDict[['_n']]
      while(nGram_flag){
        #print(i)
        #print(length(input_tokens))
        if (i>length(input_tokens)){
          break
        } 
        #print(names(p_Dict))
        if(input_tokens[i] %in% names(p_Dict)){
          r_wids<-(p_Dict[[toString(input_tokens[i])]][['_r']])
          #print(r_wids)
          if('_n' %in% names(p_Dict[[toString(input_tokens[i])]])){
            p_Dict<-p_Dict[[toString(input_tokens[i])]][['_n']]
            i<-i+1
          }
          else{
            if (i<=(length(input_tokens)-1)){
              nGram_flag<-FALSE
            }
            break
          }
        }
        else{
          nGram_flag<-FALSE
          break
        }
      }
      #print(nGram_flag)
      if (nGram_flag){
        #print(r_wids)
        output_list<<-append(output_list,r_wids)
        #print(output_list)
        if (length(output_list)<out_len){
          input_tokens_o[1]<-NULL
          predictCore(input_tokens_o,out_len = out_len)
        }
      }
      else{
        input_tokens_o[1]<-NULL
        predictCore(input_tokens_o,out_len = out_len)
      }
    }
  }
  
  predictNgram<-function(test_input,out_len=5){
    input_tokens<-cleanInputPredict(test_input)
    if (length(input_tokens)>nGramDict[['_model']]){
      input_tokens=input_tokens[(length(input_tokens)-nGramDict[['_model']]+1):length(input_tokens)]
    }
    output_list<<-list()
    output_wlist<-list()
    output<-list()
    predictCore(input_tokens,out_len = out_len)
    for (wid in output_list){
      output_wlist<-append(output_wlist,nGramDict[['_id2word']][['_id']][[wid]])
    }
    eosflag<-TRUE
    for (word in output_wlist){
      if (word=='<eos>'){
        if (eosflag){
          output<-append(output,',')
          output<-append(output,'.')
        }
        eosflag<-FALSE
      }
      else if(word=="<quantity>"){
        next
      }
      else{
        output<-append(output,word)
      }
      output_dp<-list(output[1])
      if (length(output)>1){
        for (i in 2:(length(output))){
          if (!(output[i] %in% output[1:(i-1)])){
            output_dp<-append(output_dp,output[i])
          }
        }
      }
      if (length(output)>out_len){
        output_dp=output_dp[1:out_len]
      }
    }
    out_str=""
    for (l in output_dp){
      out_str<-paste(out_str," ",l[[1]])
    }
    return(out_str)
  }

  output$value <- renderText({ predictNgram(input$caption,out_len=10) })
  
  #output$value <- renderText({ input$caption })
}

# Run the application 
shinyApp(ui = ui, server = server)

