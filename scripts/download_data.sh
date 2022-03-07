USAGE="bash download_data.sh -d [DataPath]"

while getopts d: OPT
do
    case ${OPT} in
        "d" ) OUT_DIR=${OPTARG};;
        *) echo ${USAGE}
	         exit 1 ;;
    esac
done

echo "Start downloadring training datas via ParlAI into ${OUT_DIR}/"


python ParlAI/parlai/scripts/display_data.py --task image_chat --datapath ${OUT_DIR}

DI_IMG=${OUT_DIR}/yfcc_images
DI_TXT=${OUT_DIR}/image_chat
DO_TXT=${OUT_DIR}/image_chat/filtered

python src/data/exclude_invalid_datas.py -di_img ${DI_IMG} -di_txt ${DI_TXT} -do_txt ${DO_TXT}
