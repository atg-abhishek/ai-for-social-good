//
//  ResultsViewController.swift
//  LetsTalk
//
//  Created by Arun Rawlani on 6/18/17.
//  Copyright © 2017 Arun Rawlani. All rights reserved.
//

import Foundation
import UIKit
import SwiftSpinner
import Alamofire
import SwiftyJSON

class ResultsViewController: UIViewController{
    @IBOutlet weak var timeLabel: UILabel!
    @IBOutlet weak var pauseLabel: UILabel!
    @IBOutlet weak var probLabel: UILabel!
    
    var durationString: String!
    var pauseString: String!
    var scoreString: String!
    
    var progress = 0.0
    
    override func viewDidLoad() {
        timeLabel.text = "Loading..."
        pauseLabel.text = "Loading..."
        probLabel.text = " "
        
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        
        self.demoSpinner()
        
        Alamofire.request("http://ec2-13-58-233-169.us-east-2.compute.amazonaws.com:17001/get_results").responseJSON { response in
            print("Request: \(String(describing: response.request))")   // original url request
            print("Response: \(String(describing: response.response))") // http url response
            print("Result: \(response.result)")                         // response serialization result
            
            if let json = response.result.value {
                //print("JSON: \(json)") // serialized json response
                let myJSON = JSON(json)
                let duration = myJSON["duration"].intValue
                self.durationString = String(duration)+"s"
                self.pauseString = myJSON["number_of_pauses"].stringValue
                var score = myJSON["score"].doubleValue
                var percentage = score * 100
                let rounded = Int(percentage)
                self.scoreString = String(rounded)+"%"
            }
            
            if let data = response.data, let utf8Text = String(data: data, encoding: .utf8) {
                print("Data: \(utf8Text)") // original server data as UTF8 string
            }
            
            print(self.durationString)
            print(self.pauseString)
            print(self.scoreString)
            
            self.timeLabel.text = "Loading..."
            self.pauseLabel.text = "Loading..."
            self.probLabel.text = " "
            
            self.delay(seconds: 2.0, completion: {
                self.timeLabel.text = self.durationString
                self.pauseLabel.text = self.pauseString
                self.probLabel.text = self.scoreString
            })

        }
    }
    
    
    func demoSpinner() {
        
        //SwiftSpinner.show(delay: 0.5, title: "Shouldn't see this one", animated: true)
        //SwiftSpinner.hide()
        
        SwiftSpinner.show(delay: 1.0, title: "Connecting...", animated: true)
        
        delay(seconds: 2.0, completion: {
            SwiftSpinner.show("Aggregating scores for\n pictures...")
        })
        
        delay(seconds: 6.0, completion: {
            SwiftSpinner.show("Analyzing the \n recordings")
        })
        
        delay(seconds: 10.0, completion: {
            SwiftSpinner.show("Running the model", animated: false)
        })
        
        delay(seconds: 12.0, completion: {
            SwiftSpinner.sharedInstance.outerColor = nil
            SwiftSpinner.show("Fetching the numbers")
        })
        
        delay(seconds: 14.0, completion: {
            SwiftSpinner.setTitleFont(UIFont(name: "Futura", size: 22.0))
            SwiftSpinner.sharedInstance.innerColor = UIColor.green.withAlphaComponent(0.5)
            SwiftSpinner.show(duration: 2.0, title: "Displaying Results", animated: false)
        })
        
    }
    
    func delay(seconds: Double, completion: @escaping () -> ()) {
        let popTime = DispatchTime.now() + Double(Int64( Double(NSEC_PER_SEC) * seconds )) / Double(NSEC_PER_SEC)
        
        DispatchQueue.main.asyncAfter(deadline: popTime) {
            completion()
        }
    }
    
    func timerFire(_ timer: Timer) {
        progress += (timer.timeInterval/5)
        SwiftSpinner.show(progress: progress, title: "Downloading: \(Int(progress * 100))% completed")
        if progress >= 1 {
            timer.invalidate()
            SwiftSpinner.show(duration: 2.0, title: "Complete!", animated: false)
        }
    }
    
}
