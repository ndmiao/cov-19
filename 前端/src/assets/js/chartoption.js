export const lineoption = {
    title: {
        text: '全球疫情历史数据',
        left: 'left'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['累计确诊','现存确诊','新增确诊','累计死亡','累计治愈'],
        top: '8%',
        left: 'right'
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },

    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: []
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            show: true,
            color: 'white',
            fontSize: 12,
            formatter: function(value) {
                if (value >= 10000 && value < 100000000) {
                    value = value / 10000 + '万';
                }
                else if (value >= 100000000) {
                    value = value / 100000000 + '亿';
                }
                return value;
            }
        }
    },
    series: [
        {
            name: '累计确诊',
            type: 'line',
            smooth: true,
            data: []
        },
        {
            name: '现存确诊',
            type: 'line',
            smooth: true,
            data: []
        },
        {
            name: '新增确诊',
            type: 'line',
            smooth: true,
            data: []
        },
        {
            name: '累计死亡',
            type: 'line',
            smooth: true,
            data: []
        },
        {
            name: '累计治愈',
            type: 'line',
            smooth: true,
            data: []
        }
    ]
};

export const Chinalineoption = {
    title: {
        text: '全国疫情历史数据',
        left: 'left'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['累计确诊','现存确诊','累计死亡','累计治愈'],
        top: '8%',
        left: 'right'
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },

    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: []
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            show: true,
            color: 'white',
            fontSize: 12,
            formatter: function(value) {
                if (value >= 10000 && value < 100000000) {
                    value = value / 10000 + '万';
                }
                else if (value >= 100000000) {
                    value = value / 100000000 + '亿';
                }
                return value;
            }
        }
    },
    series: [
        {
            name: '累计确诊',
            type: 'line',
            smooth: true,
            data: []
        },
        {
            name: '现存确诊',
            type: 'line',
            smooth: true,
            data: []
        },
        {
            name: '累计死亡',
            type: 'line',
            smooth: true,
            data: []
        },
        {
            name: '累计治愈',
            type: 'line',
            smooth: true,
            data: []
        }
    ]
};

export const line2option = {
    title: {
        text: '全球治愈率/病死率对比',
        left: 'left'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['病死率','治愈率'],
        top: '8%',
        left: 'right'
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },

    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: []
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            show: true,
            color: 'white',
            fontSize: 12,
            formatter: function(value) {
                value = value + '%';
                return value;
            }
        }
    },
    series: [
        {
            name: '病死率',
            type: 'line',
            smooth: true,
            data: []
        },
        {
            name: '治愈率',
            type: 'line',
            smooth: true,
            data: []
        }
    ]
};

export const Chinaline2option = {
    title: {
        text: '全国疫情新增数据',
        left: 'left'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['新增确诊','新增疑似','新增治愈','新增死亡'],
        top: '8%',
        left: 'right'
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },

    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: []
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            show: true,
            color: 'white',
            fontSize: 12,
            formatter: function(value) {
                if (value >= 10000 && value < 100000000) {
                    value = value / 10000 + '万';
                }
                else if (value >= 100000000) {
                    value = value / 100000000 + '亿';
                }
                return value;
            }
        }
    },
    series: [
        {
            name: '新增确诊',
            type: 'line',
            smooth: true,
            data: []
        },
        {
            name: '新增疑似',
            type: 'line',
            smooth: true,
            data: []
        },
        {
            name: '新增治愈',
            type: 'line',
            smooth: true,
            data: []
        },
        {
            name: '新增死亡',
            type: 'line',
            smooth: true,
            data: []
        }
    ]
};

export const baroption = {
    title: {
        text: '24小时新增确诊国家TOP6'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {            // 坐标轴指示器，坐标轴触发有效
            type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: [
        {
            type: 'category',
            data: [],
            axisTick: {
                alignWithLabel: true
            }
        }
    ],
    yAxis: [
        {   
            type: 'value',
            axisLabel: {
                show: true,
                color: 'white',
                fontSize: 12,
                formatter: function(value) {
                    if (value >= 10000 && value < 100000000) {
                        value = value / 10000 + '万';
                    }
                    else if (value >= 100000000) {
                        value = value / 100000000 + '亿';
                    }
                    return value;
                }
            }
        }
    ],
    series: [
        {
            name: '新增确诊人数',
            type: 'bar',
            barWidth: '60%',
            data: []
        }
    ]
}

export const Chinabaroption = {
    title: {
        text: '累计确诊城市TOP6(湖北除外)'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {            // 坐标轴指示器，坐标轴触发有效
            type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: [
        {
            type: 'category',
            data: [],
            axisTick: {
                alignWithLabel: true
            }
        }
    ],
    yAxis: [
        {   
            type: 'value',
            axisLabel: {
                show: true,
                color: 'white',
                fontSize: 12,
                formatter: function(value) {
                    if (value >= 10000 && value < 100000000) {
                        value = value / 10000 + '万';
                    }
                    else if (value >= 100000000) {
                        value = value / 100000000 + '亿';
                    }
                    return value;
                }
            }
        }
    ],
    series: [
        {
            name: '累计确诊人数',
            type: 'bar',
            barWidth: '60%',
            data: []
        }
    ]
}

export const pieoption = {
    title: {
        text: '各洲累计确诊人数'
    },
    tooltip: {
        trigger: 'item'
    },
    legend: {
        bottom: '0%',
        left: 'center'
    },
    series: [
        {
            name: '数据详情',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
            },
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '40',
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: [

            ]
        }
    ]
};


export const Chinapieoption = {
    title: {
        text: '各省累计确诊人数Top6'
    },
    tooltip: {
        trigger: 'item'
    },
    legend: {
        bottom: '0%',
        left: 'center'
    },
    series: [
        {
            name: '数据详情',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
            },
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '40',
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: [

            ]
        }
    ]
};


export const ChinaMapoption = {
    title: {
        text: '',
        subtext: '',
        x: 'left'
    },
    tooltip: {
        trigger: 'item'
    },
    //左侧小导航图标
    visualMap: {
        show: true,
        left: 'left',
        top: '70%',
        seriesIndex: [0],
        type:'piecewise',
        pieces:[
            {min:10000, color: '#c00'},
            {min:1000, max:9999, color: '#ff3333'},
            {min:100, max:999, color: '#ff6633'},
            {min:10, max:99, color: '#ff9933'},
            {min:1, max:9, color: '#ffcc33'}
        ],            
        textStyle: {
            color: '#white'
        }
    },     

        //配置属性
        series: [{
            name: '累积确诊人数',
            type: 'map',
            mapType: 'china',
            roam: false,
            itemStyle: {
                normal: {
                    borderWidth: .5,
                    borderColor: '#009fe8',
                    areaColor: '#ffefd5'
                },
                emphasis: {
                    borderWidth: .5,
                    borderColor: '#4b0082',
                    areaColor: '#fff'
                }
            },
            label: {
                normal: {
                    show: true, //省份名称
                    fontSize: 8
                },
                emphasis: {
                    show: true,
                    fontSize: 8
                }
            },
            data: [] //数据
        }]
    };



export const globaloption = {

    tooltip: {
        trigger: 'item',
        formatter: function(params) {                        
                var toolTiphtml = ''
                if (isNaN(params.value)){
                toolTiphtml = params.name + '累计确诊: 0例';
                }
                else{
                toolTiphtml = params.name + '累计确诊: ' + params.value + '例';
                }
                //console.log(toolTiphtml)                        
                return toolTiphtml;                   
        }
    },

    visualMap: {
        show: true,
        left: 'left',
        top: '60%',
        seriesIndex: [0],
        type:'piecewise',
        pieces:[
            {min:1000000, color: '#c00'},
            {min:100000, max:999999, color: '#ff3333'},
            {min:10000, max:99999, color: '#ff6633'},
            {min:1000, max:9999, color: '#ff6633'},
            {min:1, max:999, color: '#ffcc33'}
        ],            
        textStyle: {
            color: '#white'
        }
    },            
    geo: {
        show: true,
        map: 'world',
        label: {
            normal: {
                show: false,
                fontSize:12,
            },
            emphasis: {
                show: false,
            }
        },
        roam: true,
        
        itemStyle: {
            normal: {
                areaColor: '#F6F6F6',
                borderColor: '#666666',
            },
            emphasis: {
                areaColor: '#0099CC',
            }
        }
    },
    series: [
        {
            type: 'map',
            map: 'world',
            geoIndex: 0,           
            animation: false,
            data: []
        },
    ]    
};





