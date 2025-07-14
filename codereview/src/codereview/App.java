package com.ad.java.practice;


import com.google.gson.Gson;
import org.apache.poi.hpsf.Decimal;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;


import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class App {



    public static void main(String[] args) {
        System.out.println("START");

        loadExcelToJSON("/ExampleSheet.xlsx");
        System.out.println("END");
    }

    static void loadExcelToJSON(String filePath) {

        try (

                InputStream inputStream = App.class.getResourceAsStream(filePath);
                Workbook wb = new XSSFWorkbook(inputStream)
        ) {
            for (int i = 0; i < wb.getNumberOfSheets(); i++) {
                Sheet sheet = wb.getSheetAt(i);
                Map<Integer, String> headersMap = new HashMap();
                Map<String,Double> rowMap = new HashMap<>();
                List<Map> listOfRowMaps = new ArrayList<>();

                System.out.println(wb.getSheetName(i));
                for (Row row : sheet) {
                    int rownum = row.getRowNum();
                    if (rownum == 0){
                        for (Cell cell : row) {
                            headersMap.put(cell.getColumnIndex(), cell.getStringCellValue());
                        }
                    }
                    else{
                        for (Cell cell : row) {
                            rowMap.put(headersMap.get(cell.getColumnIndex()),cell.getNumericCellValue());
                        }
                        listOfRowMaps.add(rowMap);
                    }


                }
                Gson gson = new Gson();
                String jsonArray = gson.toJson(listOfRowMaps);
                System.out.println(jsonArray);
            }

        } catch (IOException e) {
            throw new RuntimeException(e);
        }

    }
}
